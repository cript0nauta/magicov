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
            # if not node.args.defaults and not node.decorator_list:
            if False:
                # This is needed to get 100% coverage, but can be buggy in some
                # edge cases. I'll ignore this for now
                # Returning None will break functions whose arguments or decorators
                # have side effects
                assigned_value = ast.Str(s='I was an unused function in the past')
                assigned_value = ast.Lambda(
                    args=ast.arguments(
                        args=[ast.Name(id='x')],
                        vararg=None,
                        kwarg=None,
                        defaults=[],
                    ),
                    body=ast.Name(id='x')
                )
                return ast.Assign(
                    targets=[ast.Name(id=node.name)],
                    value=assigned_value,
                )
            node.body = [ast.copy_location(ast.Pass(), node.body[0])]
            # function_call = ast.Call(
            #     func=ast.Name(id=node.name),
            #     args=[],
            #     keywords=[],
            #     starargs=[],
            #     kwargs=[],
            # )
            # return [node, function_call]
            return node
        else:
            return node


def main():
    if len(sys.argv) >= 2:
        covfile = sys.argv[1]
    else:
        covfile = '.coverage'
    data = coverage.CoverageData()
    data.read_file(covfile)

    for filename in data._lines:
        lines = data.lines(filename)
        assert lines is not None
        if not os.path.exists(filename):
            # It could be unlinked before
            continue
        if not lines:
            print filename, 'not covered, removing'
            os.unlink(filename)
            continue
        with open(filename) as fp:
            tree = pasta.parse(fp.read())
        new_tree = rewrite(tree, lines)

        try:
            to_write = pasta.dump(new_tree)
        except pasta.base.codegen.PrintError:
            print "Error with file", filename
            continue

        with open(filename, 'w') as fp:
            fp.write(to_write)


if __name__ == '__main__':
    main()
