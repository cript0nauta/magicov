import os
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


def main():
    for filename, module_name in discover_tests():
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
        code = compile(new_tree, filename, 'exec')
        print 'executing rewritten code'
        exec(code)


if __name__ == '__main__':
    main()
