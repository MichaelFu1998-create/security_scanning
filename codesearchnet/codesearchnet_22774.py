def check_path_action(self):
        """ custom command line action to check file exist """
        class CheckPathAction(argparse.Action):
            def __call__(self, parser, args, value, option_string=None):
                if type(value) is list:
                    value = value[0]
                user_value = value
                if option_string == 'None':
                    if not os.path.isdir(value):
                        _current_user = os.path.expanduser("~")
                        if not value.startswith(_current_user) \
                                and not value.startswith(os.getcwd()):
                            if os.path.isdir(os.path.join(_current_user, value)):
                                value = os.path.join(_current_user, value)
                            elif os.path.isdir(os.path.join(os.getcwd(), value)):
                                value = os.path.join(os.getcwd(), value)
                            else:
                                value = None
                        else:
                            value = None
                elif option_string == '--template-name':
                    if not os.path.isdir(value):
                        if not os.path.isdir(os.path.join(args.target, value)):
                            value = None
                if not value:
                    logger.error("Could not to find path %s. Please provide "
                                 "correct path to %s option",
                                 user_value, option_string)
                    exit(1)
                setattr(args, self.dest, value)

        return CheckPathAction