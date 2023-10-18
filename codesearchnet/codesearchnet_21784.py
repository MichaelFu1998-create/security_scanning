def _pre_activate(self):
        '''
        Prior to activating, store everything necessary to deactivate this
        environment.
        '''

        if 'CPENV_CLEAN_ENV' not in os.environ:
            if platform == 'win':
                os.environ['PROMPT'] = '$P$G'
            else:
                os.environ['PS1'] = '\\u@\\h:\\w\\$'
            clean_env_path = utils.get_store_env_tmp()
            os.environ['CPENV_CLEAN_ENV'] = clean_env_path
            utils.store_env(path=clean_env_path)
        else:
            utils.restore_env_from_file(os.environ['CPENV_CLEAN_ENV'])