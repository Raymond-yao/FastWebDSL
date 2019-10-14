class Component:
    GLOBAL_DEFAULT_ARGS = {
        "className": ""
    }

    def __init__(self, component, defaultArgs, args, rows, argToAttrMap={}):
        self.component = component
        self.args = {**self.GLOBAL_DEFAULT_ARGS, **defaultArgs, **args}
        if len(self.args.keys()) != len({**self.GLOBAL_DEFAULT_ARGS, **defaultArgs}.keys()):
            raise UnknownArgError(component, defaultArgs.keys())
        for key in self.args.keys():
            # I'm forcing the parameters to be type of strings
            # then argToAttrMap deals with detailed attr values
            if type(self.args[key]) is not str:
                raise UnknownValueError(key, "strings")
            if key in argToAttrMap.keys() and self.args[key] not in argToAttrMap[key].keys():
                raise UnknownValueError(key, argToAttrMap[key].keys())
        self.rows = rows

    def render(self):
        raise Exception("Render method of this componet is not implemented!")

    def getParamVal(self, param):
        if param not in self.args.keys():
            raise UnknownArgError(self.component, self.args)
        return self.args[param]


class EvaluationError(Exception):
    def __init__(self, componet, err):
        message = """
        Evalution Error: Unable to form a resonable layout for %s.
        Please make sure %s
        """ % (componet, err)
        super().__init__(message)


class UnknownArgError(Exception):
    def __init__(self, component, expectedArgs):
        super().__init__("Unknown Argument: component %s only expects %s" %
                         (component, list(expectedArgs)))


class UnknownValueError(Exception):
    def __init__(self, arg, expectedValues):
        super().__init__("Unknown Value: % arguement only expects one of %s" %
                         (arg, list(expectedValues)))
