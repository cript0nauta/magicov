import ast
import sys
import importlib
import pasta
import coverage

def rewrite(tree, lines):
    FuncRemover(lines).visit(tree)
    return tree


class FuncRemover(ast.NodeTransformer):
    def __init__(self, lines):
        self.lines = lines

    def visit_FunctionDef(self, node):
        if node.body[0].lineno not in self.lines:
            return None
        else:
            return node


def main():
    if len(sys.argv) >= 2:
        module = sys.argv[1]
    else:
        module = 'test_unused_function'
    cov = coverage.Coverage()
    cov.start()
    importlib.import_module(module)
    cov.stop()
    data = cov.get_data()

    for filename in data._lines:
        if 'magicov' not in filename:
            continue
        print "Rewriting", filename
        lines = data.lines(filename)
        assert lines is not None
        with open(filename) as fp:
            tree = pasta.parse(fp.read())
        new_tree = rewrite(tree, lines)
        print pasta.dump(new_tree)


if __name__ == '__main__':
    main()
