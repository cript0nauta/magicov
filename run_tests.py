import os
import ast
import glob
import importlib
import coverage
import pasta
from magicov import rewrite
import tests.side_effect_utils


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
        print 'testing', module_name, filename
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

        new_filename = os.path.join(
            os.path.dirname(os.path.dirname(filename)),
            'rewritten_tests',
            os.path.basename(filename)
        )
        with open(new_filename, 'w') as fp:
            fp.write(pasta.dump(new_tree))
        new_module_name = module_name.replace('tests.', 'rewritten_tests.')

        tests.side_effect_utils.c.reset()
        cov_rewrite = coverage.Coverage(include=[new_filename])
        cov_rewrite.start()
        importlib.import_module(new_module_name)
        cov_rewrite.stop()

        (filename2, executable, notrun, notrun_fmt) = cov_rewrite.analysis(new_filename)
        assert new_filename == filename2
        assert len(notrun) == 0, (
            "File {} did not get 100% coverage. "
            "Lines missed: {}".format(
                new_filename, notrun_fmt)
        )


if __name__ == '__main__':
    main()
