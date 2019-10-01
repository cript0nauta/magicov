import os
import ast
import sys
import importlib
import pasta
import coverage

def rewrite(tree, lines):
    FuncRemover(lines).visit(tree)
    IfRemover(lines).visit(tree)
    BodyRemover(lines).visit(tree)
    return tree


class BaseRemover(ast.NodeTransformer):
    def __init__(self, lines):
        self.lines = lines

    def is_body_covered(self, stmts, allow_no_lineno=False):
        if allow_no_lineno:
            return any(getattr(stmt, 'lineno', -1) in self.lines for stmt in stmts)
        else:
            return any(stmt.lineno in self.lines for stmt in stmts)


class FuncRemover(BaseRemover):
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


class IfRemover(BaseRemover):
    def visit_If(self, node):
        if node.orelse and not self.is_body_covered(node.orelse):
            # Remove the `else` part of the `if` if it's not covered
            node.orelse = []
        elif not self.is_body_covered(node.body):
            # The main part of the `if` is not covered
            if node.orelse and isinstance(node.orelse[0], ast.If):
                # This is probably an elif clause
                node.orelse[0] = self.visit_If(node.orelse[0])

                new_test = ast.BoolOp(
                    op=ast.Or(),
                    values=[node.test, node.orelse[0].test]
                )

                node.test = new_test
                node.body = node.orelse[0].body
                node.orelse = node.orelse[0].orelse
            elif node.orelse:
                # Only the `else` part is covered. Move the `else` part to the
                # main part removing the previous uncovered content. Make sure
                # the `test` stills being executed to maintain the software
                # behavior, even when the `test` has side effects.

                # Because the main part of the `if` is uncovered, we can assume
                # that the `test` always evaluates to False.

                new_test = ast.BoolOp(
                    op=ast.Or(),
                    values=[node.test, ast.Name(id='True')]
                )
                node.test = new_test
                node.body = node.orelse
                node.orelse = []
            else:
                # The `if` doesn't have an `else` block

                # This would be better, but causes intentarion errors in some
                # conditions.
                # return [ast.Expr(node.test)]

                new_test = ast.BoolOp(
                    op=ast.Or(),
                    values=[node.test, ast.Name(id='True')]
                )
                node.test = new_test
                node.body = [ast.Pass()]
                node.orelse = []

        return node


class BodyRemover(BaseRemover):
    def generic_visit(self, node):
        new_node = super(BaseRemover, self).generic_visit(node)
        if hasattr(new_node, 'body') and isinstance(new_node.body, list) \
                and self.is_body_covered(new_node.body, allow_no_lineno=True):
            reached_stmts = [new_node.body[0]]  # There has to be at least one stmt
            unreached_stmts = []
            for stmt in new_node.body[1:]:
                if getattr(stmt, 'lineno', -1) in self.lines:
                    # Some statements never have coverage. If there is a statement
                    # below them, we can assume it has been covered
                    reached_stmts += unreached_stmts
                    unreached_stmts = []

                    # The node covered is logically covered
                    reached_stmts.append(stmt)
                else:
                    unreached_stmts.append(stmt)
            new_node.body = reached_stmts
        return new_node


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
