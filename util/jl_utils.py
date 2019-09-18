class Testable:

    def __init__(self, call, test_args, test_kwargs):
        self.call = call
        self.test_args = test_args
        self.test_kwargs = test_kwargs

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    def test(self):
        return self.call(*self.test_args, **self.test_kwargs)

def with_test(*args, **kwargs):
    def inner(func):
        res = Testable(func, args, kwargs)
        return res
    return inner

