import os
import ast
import glob
import importlib
import coverage
import pasta
from magicov import rewrite


def discover_tests():
    for filename in glob.glob('tests/*.py'):
        if not os.path.basename(filename).startswith('test'):
            continue
        fullpath = os.path.abspath(filename)
        module_name = filename.replace('/', '.')
        module_name = module_name[:-3]  # Remove the .py
        yield fullpath, module_name


def assert_no_removemes(tree):
    visitor = RemovemeVisitor()
    visitor.visit(tree)
    assert not visitor.lines_with_removeme, \
        "Found some lines with a removeme in lines: %s" % \
        visitor.lines_with_removeme


class RemovemeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.lines_with_removeme = []

    def visit_Name(self, node):
        if node.id == 'removeme':
            self.lines_with_removeme.append(node.lineno)


def main():
    for filename, module_name in discover_tests():
        print 'testing', module_name
        cov = coverage.Coverage(include=[filename])
        cov.start()
        importlib.import_module(module_name)
        cov.stop()

        data = cov.get_data()
        lines = data.lines(filename)
        assert lines is not None, data._lines.keys()

        with open(filename) as fp:
            tree = pasta.parse(fp.read())

        new_tree = rewrite(tree, lines)
        assert_no_removemes(new_tree)
        code = compile(new_tree, filename, 'exec')
        print 'executing rewritten code'
        exec(code)


if __name__ == '__main__':
    main()
