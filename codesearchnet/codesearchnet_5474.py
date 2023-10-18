def _get_blockade_id_from_cwd(self, cwd=None):
        '''Generate a new blockade ID based on the CWD'''
        if not cwd:
            cwd = os.getcwd()
        # this follows a similar pattern as docker-compose uses
        parent_dir = os.path.abspath(cwd)
        basename = os.path.basename(parent_dir).lower()
        blockade_id = re.sub(r"[^a-z0-9]", "", basename)
        if not blockade_id:  # if we can't get a valid name from CWD, use "default"
            blockade_id = "default"
        return blockade_id