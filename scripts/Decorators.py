def ParamsToObjectVar(function):
    def decorator_params(self, args):
        for key, value in args.items():
            self.__setattr__(key, value)
        return function(self, args)
    return decorator_params