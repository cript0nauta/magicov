def deco(f):
    return f

@deco
def unused():
    removeme
    removeme
    return 8

@deco
def used():
    return 42

used()
