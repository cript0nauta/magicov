import sys
import ast
import pasta

with open(sys.argv[1]) as fp:
    a = pasta.parse(fp.read())
    print(ast.dump(a))
