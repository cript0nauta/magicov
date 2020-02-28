import os
import ast
import sys
import click
import importlib
import pasta
import coverage

def rewrite(tree, lines):
    LinenoEndAdder().visit(tree)
    FuncRemover(lines).visit(tree)
    IfRemover(lines).visit(tree)
    LoopRemover(lines).visit(tree)
    ExceptRemover(lines).visit(tree)
    BodyRemover(lines).visit(tree)
    YieldAdder(lines).visit(tree)
    return tree


generator_function_nodes = set()


class BaseRemover(ast.NodeTransformer):
    def __init__(self, lines):
        self.lines = lines

    def is_body_covered(self, stmts, allow_no_lineno=False):
        return any(self.is_stmt_covered(stmt, allow_no_lineno) for stmt in stmts)

    def is_stmt_covered(self, stmt, allow_no_lineno=True):
        if hasattr(stmt, 'lineno_end'):
            assert stmt.lineno_end >= stmt.lineno
            return any(
                line in self.lines
                for line in range(stmt.lineno, stmt.lineno_end+1)
            )
        try:
            return stmt.lineno in self.lines
        except AttributeError:
            if allow_no_lineno:
                return False
            raise


class FuncRemover(BaseRemover):
    def visit_FunctionDef(self, node):
        if is_generator_function(node):
            generator_function_nodes.add(node)
        if not self.is_body_covered(node.body):
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

            inner_node = ast.Pass()
            inner_node.__pasta__ = {'suffix': '  # pragma: no cover\n'}
            node.body = [ast.copy_location(inner_node, node.body[0])]
            # function_call = ast.Call(
            #     func=ast.Name(id=node.name),
            #     args=[],
            #     keywords=[],
            #     starargs=[],
            #     kwargs=[],
            # )
            # return [node, function_call]
        super(FuncRemover, self).generic_visit(node)
        return node


def is_generator_function(node):
    has_yield = False

    class YieldVisitor(BaseRemover):
        def __init__(self):
            return

        def visit_Yield(self, node):
            nonlocal has_yield
            has_yield = True
            return node

        def visit(self, child_node):
            if isinstance(child_node, ast.FunctionDef) and \
                    child_node is not node:
                # This is another function definition, so stop recursion
                return child_node
            return super(YieldVisitor, self).visit(child_node)

    YieldVisitor().visit(node)
    return has_yield


class IfRemover(BaseRemover):
    def visit_If(self, node):
        if node.orelse and not self.is_body_covered(node.orelse):
            # Remove the `else` part of the `if` if it's not covered
            node.orelse = []
        elif not self.is_body_covered(node.body):
            # The main part of the `if` is not covered
            if node.orelse and len(node.orelse) == 1 and \
                    isinstance(node.orelse[0], ast.If):
                # This is probably an elif clause
                node.orelse[0] = self.visit_If(node.orelse[0])

                # This hack fixes bad indentation of the `else` part
                orelse_pasta = node.orelse[0].__pasta__
                if orelse_pasta.get('is_elif') and 'elseprefix' in orelse_pasta:
                    node.__pasta__['elseprefix'] = orelse_pasta['elseprefix']

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

                # This would be better, but causes indentation errors in some
                # conditions.
                # return [ast.Expr(node.test)]

                new_test = ast.BoolOp(
                    op=ast.Or(),
                    values=[node.test, ast.Name(id='True')]
                )
                node.test = new_test
                node.body = [ast.copy_location(ast.Pass(), node.body[0])]
                node.orelse = []

        super(IfRemover, self).generic_visit(node)
        return node


class LoopRemover(BaseRemover):
    def visit_For(self, node):
        if not self.is_body_covered(node.body):
            test = ast.BoolOp(
                op=ast.Or(),
                values=[node.iter, ast.Name(id='True')]
            )
            body = [ast.copy_location(ast.Pass(), node.body[0])]
            if_ = ast.If(test=test, body=body, orelse=[])
            # This is a workaround on a pasta bug
            # TODO remove when is is fixed
            if_.__pasta__ = {'prefix': node.__pasta__['prefix']}
            return if_
        elif node.orelse and not self.is_body_covered(node.orelse):
            node.orelse = []
        return super(LoopRemover, self).generic_visit(node)

    def visit_While(self, node):
        if not self.is_body_covered(node.body):
            test = ast.BoolOp(
                op=ast.Or(),
                values=[node.test, ast.Name(id='True')]
            )
            body = [ast.copy_location(ast.Pass(), node.body[0])]
            if_ = ast.If(test=test, body=body, orelse=[])
            # This is a workaround on a pasta bug
            # TODO remove when is is fixed
            if_.__pasta__ = {'prefix': node.__pasta__['prefix']}
            return if_
        elif node.orelse and not self.is_body_covered(node.orelse):
            node.orelse = []
        return super(LoopRemover, self).generic_visit(node)


class BodyRemover(BaseRemover):
    def generic_visit(self, node):
        new_node = super(BaseRemover, self).generic_visit(node)
        if hasattr(new_node, 'body') and isinstance(new_node.body, list) \
                and self.is_body_covered(new_node.body, allow_no_lineno=True):
            reached_stmts = [new_node.body[0]]  # There has to be at least one stmt
            unreached_stmts = []
            for stmt in new_node.body[1:]:
                if self.is_stmt_covered(stmt):
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


class YieldAdder(BaseRemover):
    """If all `yield`s of a function are removed, it will be directly executed
    when rewritten instead of returning a generator. This rewriter adds a never
    covered yield statement to force the function to return generators."""
    def visit_FunctionDef(self, node):
        if node in generator_function_nodes and \
                not is_generator_function(node):
            return_node = ast.copy_location(
                ast.Return(value=None), node.body[-1])
            return_node.__pasta__ = {'suffix': '  # pragma: no cover\n'}
            node.body.append(return_node)

            yield_node = ast.copy_location(
                ast.Expr(ast.Yield(value=None)), node.body[-1])
            yield_node.__pasta__ = {'suffix': '  # pragma: no cover\n'}
            node.body.append(yield_node)

        super(YieldAdder, self).generic_visit(node)
        return node


class LinenoEndAdder(ast.NodeVisitor):
    """The "lineno" attribute of nodes indicates the line where the
    block/statement starts. We also need the line where it ends.

    To do this, recursively iterate over the node childs, and fetch
    the maximum lineno.
    """

    def generic_visit(self, node):
        try:
            lineno = node.lineno
        except AttributeError:
            # lineno_end is useless without lineno. We can use the super
            # method
            return super(LinenoEndAdder, self).generic_visit(node)

        try:
            lineno_end = node.lineno
        except AttributeError:
            lineno_end = -1

        def check_node_lineno(node):
            nonlocal lineno_end
            if not hasattr(node, 'lineno_end'):
                return
            lineno_end = max(lineno_end, node.lineno_end)

        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
                        check_node_lineno(item)
            elif isinstance(value, ast.AST):
                self.visit(value)
                check_node_lineno(value)

        if lineno_end != -1:
            node.lineno_end = lineno_end
        return node


class ExceptRemover(BaseRemover):
    def visit_Try(self, node):
        node.handlers = [
            handler
            for handler in node.handlers
            if (self.is_body_covered(handler.body) or
                (handler.type and self.is_stmt_covered(handler.type) and not self.is_static_expr(handler.type)))
        ]
        if not node.handlers and not node.finalbody:
            # We can't make a try without an except and a finally, so convert
            # it to an "if True:" block
            if_ = ast.If(
                test=ast.Name(id='True'),
                body=node.body + node.orelse,
                orelse=[],
            )

            # This is a workaround on a pasta bug
            # TODO remove when is is fixed
            if_.__pasta__ = {'prefix': node.__pasta__['prefix']}
            # assert if_.__pasta__['indent'] < node.body[0].__pasta__['indent'], \
            #         ("The if: block has the same indentation as its body. This "
            #          "will cause an IndentationError in the rewritten code.")

            return super(ExceptRemover, self).generic_visit(
                ast.copy_location(if_, node))

        if not self.is_body_covered(node.orelse):
            node.orelse = []

        return super(ExceptRemover, self).generic_visit(node)

    @staticmethod
    def is_static_expr(expr):
        """Return true if we can assume the expression doesn't have
        side effects"""
        return isinstance(expr, ast.Name)


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.command()
@click.option(
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    help="Disable the prompt asking the user to confirm the operation",
    prompt=(
        "WARNING: This is a joke project. The operation being executed will "
        "modify your source code and make it unusable in any place other than "
        "your test suite. Have you already done a backup of all files listed "
        "when you run `coverage report`?"
    )
)
@click.argument('coverage_file', default='.coverage')
def main(coverage_file):
    data = coverage.CoverageData()
    data.read_file(coverage_file)

    for filename in data._lines:
        lines = data.lines(filename)
        assert lines is not None
        if not os.path.exists(filename):
            # It could be unlinked before
            continue
        if not lines:
            print(filename, 'not covered, removing')
            os.unlink(filename)
            continue
        with open(filename) as fp:
            tree = pasta.parse(fp.read())
        new_tree = rewrite(tree, lines)

        try:
            to_write = pasta.dump(new_tree)
        except pasta.base.codegen.PrintError:
            print("Error with file", filename)
            continue

        with open(filename, 'w') as fp:
            fp.write(to_write)


if __name__ == '__main__':
    main()
