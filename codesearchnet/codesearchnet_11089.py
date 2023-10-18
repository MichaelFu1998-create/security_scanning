def reload_programs(self):
        """
        Reload all shader programs with the reloadable flag set
        """
        print("Reloading programs:")
        for name, program in self._programs.items():
            if getattr(program, 'program', None):
                print(" - {}".format(program.meta.label))
                program.program = resources.programs.load(program.meta)