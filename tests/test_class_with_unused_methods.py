# This is commented because of the added pragma: nocov
# _magicov_expected_uncovered_lines = 3

class Test:
    def method1(self):
        removeme

    def method2(self):
        removeme

    def method3(self):
        removeme

    def unused_generator(self):
        # This function is not covered at first because it has a yield,
        # but will be covered after being rewritten.
        n=1
        removeme
        yield 1

    def used_generator(self):
        yield 1

Test().unused_generator()
next(Test().used_generator())
