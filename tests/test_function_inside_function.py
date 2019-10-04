def f():
    def f2():
        removeme
        removeme
    return 5

f()
