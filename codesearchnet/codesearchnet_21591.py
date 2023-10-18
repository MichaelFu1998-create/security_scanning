def get_parameters(self):
        """Returns a list of parameters"""
        if self.plugin_class is None:
            sig = inspect.signature(self.func)
            for index, parameter in enumerate(sig.parameters.values()):
                if not parameter.kind in [parameter.POSITIONAL_ONLY, parameter.KEYWORD_ONLY, parameter.POSITIONAL_OR_KEYWORD]:
                    raise RuntimeError("Task {} contains an unsupported {} parameter".format(parameter, parameter.kind))

                yield parameter

        else:
            var_keyword_seen = set()

            for cls in inspect.getmro(self.plugin_class):
                if issubclass(cls, BasePlugin) and hasattr(cls, self.func.__name__):
                    func = getattr(cls, self.func.__name__)
                    logger.debug("Found method %s from class %s", func, cls)
                    var_keyword_found = False
                    sig = inspect.signature(func)
                    for index, parameter in enumerate(sig.parameters.values()):
                        if index == 0:
                            # skip "self" parameter
                            continue

                        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
                            # found "**kwargs" parameter.  we will continue to the next class in the mro
                            # to add any keyword parameters we have not yet used (i.e. whose name
                            # we have not yet seen)
                            var_keyword_found = True
                            continue

                        if parameter.kind in [parameter.POSITIONAL_ONLY, parameter.VAR_POSITIONAL]:
                            raise RuntimeError("Task {} contains an unsupported parameter \"{}\"".format(func, parameter))

                        if not parameter.name in var_keyword_seen:
                            var_keyword_seen.add(parameter.name)

                            logger.debug("Found parameter %s (%s)", parameter, parameter.kind)
                            yield parameter

                    # we only need to look at the next class in the mro
                    # when "**kwargs" is found
                    if not var_keyword_found:
                        break