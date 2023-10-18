def _call(self, func, this, args):
        ''' Calls a bytecode function func
            NOTE:  use !ONLY! when calling functions from native methods! '''
        assert not func.is_native
        # fake call - the the runner to return to the end of the file
        old_contexts = self.contexts
        old_return_locs = self.return_locs
        old_curr_ctx = self.current_ctx

        self.contexts = [FakeCtx()]
        self.return_locs = [len(self.tape)]  # target line after return

        # prepare my ctx
        my_ctx = func._generate_my_context(this, args)
        self.current_ctx = my_ctx

        # execute dunction
        ret = self.run(my_ctx, starting_loc=self.label_locs[func.code])

        # bring back old execution
        self.current_ctx = old_curr_ctx
        self.contexts = old_contexts
        self.return_locs = old_return_locs

        return ret