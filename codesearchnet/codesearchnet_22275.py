def get_state(self):
        """Get the current directory state"""
        return [os.path.join(dp, f)
                for dp, _, fn in os.walk(self.dir)
                for f in fn]