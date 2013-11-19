class FunctionRegistry:
    def __init__(self):
        self.funcs = {}

    def register(self, func):
        self.funcs[func.__name__] = func
        return func

    def get(self, name):
        return self.funcs[name]

    def func_names(self):
        return self.funcs.keys()

all_features = {}
