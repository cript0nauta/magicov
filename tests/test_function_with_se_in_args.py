try:
    from side_effect_utils import c
except ImportError:
    # TODO: unify the imports to be the same
    # before and after rewriting
    from tests.side_effect_utils import c

def removemybody(a=c(1), b=c(2)):
    removeme

c(3)
