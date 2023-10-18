def get_reference_to_class(cls, class_or_class_name):
        """
        Detect if we get a class or a name, convert a name to a class.
        """
        if isinstance(class_or_class_name, type):
            return class_or_class_name

        elif isinstance(class_or_class_name, string_types):
            if ":" in class_or_class_name:
                mod_name, class_name = class_or_class_name.split(":")

                if not mod_name in sys.modules:
                    __import__(mod_name)

                mod = sys.modules[mod_name]
                return mod.__dict__[class_name]

            else:
                return cls.load_class_from_locals(class_or_class_name)

        else:
            msg = "Unexpected Type '%s'" % type(class_or_class_name)
            raise InternalCashewException(msg)