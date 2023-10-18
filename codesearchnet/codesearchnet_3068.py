def execute_fragment_under_context(self, ctx, start_label, end_label):
        ''' just like run but returns if moved outside of the specified fragment
            # 4 different exectution results
            # 0=normal, 1=return, 2=jump_outside, 3=errors
            # execute_fragment_under_context returns:
            # (return_value, typ, return_value/jump_loc/py_error)
            # IMPARTANT: It is guaranteed that the length of the ctx.stack is unchanged.
        '''
        old_curr_ctx = self.current_ctx
        self.ctx_depth += 1
        old_stack_len = len(ctx.stack)
        old_ret_len = len(self.return_locs)
        old_ctx_len = len(self.contexts)
        try:
            self.current_ctx = ctx
            return self._execute_fragment_under_context(
                ctx, start_label, end_label)
        except JsException as err:
            if self.debug_mode:
                self._on_fragment_exit("js errors")
            # undo the things that were put on the stack (if any) to ensure a proper error recovery
            del ctx.stack[old_stack_len:]
            del self.return_locs[old_ret_len:]
            del self.contexts[old_ctx_len :]
            return undefined, 3, err
        finally:
            self.ctx_depth -= 1
            self.current_ctx = old_curr_ctx
            assert old_stack_len == len(ctx.stack)