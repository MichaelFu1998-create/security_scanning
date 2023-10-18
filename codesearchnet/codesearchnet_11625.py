def getScript(self, scriptname):
        ''' Return the specified script command. If the first part of the
            command is a .py file, then the current python interpreter is
            prepended.

            If the script is a single string, rather than an array, it is
            shlex-split.
        '''
        script = self.description.get('scripts', {}).get(scriptname, None)
        if script is not None:
            if isinstance(script, str) or isinstance(script, type(u'unicode string')):
                import shlex
                script = shlex.split(script)
            # if the command is a python script, run it with the python
            # interpreter being used to run yotta, also fetch the absolute path
            # to the script relative to this module (so that the script can be
            # distributed with the module, no matter what current working
            # directory it will be executed in):
            if len(script) and script[0].lower().endswith('.py'):
                if not os.path.isabs(script[0]):
                    absscript = os.path.abspath(os.path.join(self.path, script[0]))
                    logger.debug('rewriting script %s to be absolute path %s', script[0], absscript)
                    script[0] = absscript
                import sys
                script = [sys.executable] + script

        return script