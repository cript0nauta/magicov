def deco(f):
    return f

@deco
def unused(removeme):
    1/1
    return 8

@deco
def used():
    return 42


print used()
