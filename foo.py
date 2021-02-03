

def test(a, b, *, c, **kw):
    print(a, b, c)
    print(kw)


test(5, 1, 60, c=10)
