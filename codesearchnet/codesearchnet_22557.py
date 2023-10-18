def _get_classes(package_name, base_class):
        """
        search monits or works classes. Class must have 'name' attribute
        :param package_name: 'monits' or 'works'
        :param base_class: Monit or Work
        :return: tuple of tuples monit/work-name and class
        """
        classes = {}

        base_dir = os.getcwd()
        root_module_name = base_dir.split('/')[-1]
        package_dir = base_dir + '/%s' % package_name
        if os.path.isdir(package_dir):
            for module_path in os.listdir(package_dir):
                if not module_path.endswith('.py'):
                    continue

                module_name = os.path.splitext(module_path)[0]
                module_full_name = '%s.%s.%s' % (root_module_name, package_name, module_name)
                __import__(module_full_name)
                work_module = sys.modules[module_full_name]
                for module_item in work_module.__dict__.values():
                    if type(module_item) is type \
                            and issubclass(module_item, base_class) \
                            and module_item is not base_class\
                            and hasattr(module_item, 'name') and module_item.name:
                        classes.setdefault(module_item.name, []).append(module_item)

        # check no duplicated names
        for work_name, work_modules in classes.items():
            if len(work_modules) > 1:
                raise DuplicatedNameException('Modules %s have same name "%s"' % (
                    ' and '.join(map(str, work_modules)),
                    work_name
                ))

        # create immutable list of modules
        return tuple([(work_name, work_modules[0]) for work_name, work_modules in classes.items()])