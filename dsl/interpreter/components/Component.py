class Component:
    GLOBAL_DEFAULT_ARGS = {
        "className": ""
    }

    def __init__(self, component, defaultArgs, args, rows, argsToAttrMap={}):
        self.component = component
        self.args = {**self.GLOBAL_DEFAULT_ARGS, **defaultArgs, **args}
        if len(self.args.keys()) != len(defaultArgs.keys()):
            raise UnknownArgError(component, defaultArgs.keys())
        for key in self.args.keys():
            if key in argsToAttrMap.keys() and self.args[key] not in argsToAttrMap[key].values():
                raise UnknownValueError(key, argsToAttrMap[key].values())
        self.rows = rows

    def render(self):
        raise Exception("Render method of this componet is not implemented!")

    def getParamVal(self, param):
        if param not in self.args.keys():
            raise UnknownArgError(param, self.component)
        return self.args[param]


class EvaluationError(Exception):
    def __init__(self, componet, err):
        message = """
        Evalution Error: Unable to form a resonable layout for %s.
        Please make sure %s
        """ % (componet, err)
        super().__init__(message)


class UnknownArgError(Exception):
    def __init__(self, expectedArgs, component):
        super().__init__("Unknown Argument: component %s only expects %s" %
                         (component, list(expectedArgs)))


class UnknownValueError(Exception):
    def __init__(self, arg, expectedValues):
        super().__init__("Unknown Value: % arguement only expects one of %s" %
                         (arg, list(expectedValues)))
