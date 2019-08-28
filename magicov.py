import os
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
        is_function_covered = any(stmt.lineno in self.lines for stmt in node.body)
        if not is_function_covered:
            if not node.args.defaults and not node.decorator_list:
                # Returning None will break functions whose arguments or decorators
                # have side effects
                return None
            node.body = [ast.copy_location(ast.Pass(), node.body[0])]
            function_call = ast.Call(
                func=ast.Name(id=node.name),
                args=[],
                keywords=[],
                starargs=[],
                kwargs=[],
            )
            return [node, function_call]
        else:
            return node


def main():
    if len(sys.argv) >= 2:
        module = sys.argv[1]
    else:
        module = 'tests.test_unused_function'
    cov = coverage.Coverage()
    cov.start()
    importlib.import_module(module)
    cov.stop()
    data = cov.get_data()

    for filename in data._lines:
        if 'magicov' not in filename:
            continue
        if not os.path.basename(filename).startswith('test_'):
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
