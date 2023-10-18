def handle_app_update(self, task_id, future, memo_cbk=False):
        """This function is called as a callback when an AppFuture
        is in its final state.

        It will trigger post-app processing such as checkpointing
        and stageout.

        Args:
             task_id (string) : Task id
             future (Future) : The relevant app future (which should be
                 consistent with the task structure 'app_fu' entry

        KWargs:
             memo_cbk(Bool) : Indicates that the call is coming from a memo update,
             that does not require additional memo updates.
        """

        if not self.tasks[task_id]['app_fu'].done():
            logger.error("Internal consistency error: app_fu is not done for task {}".format(task_id))
        if not self.tasks[task_id]['app_fu'] == future:
            logger.error("Internal consistency error: callback future is not the app_fu in task structure, for task {}".format(task_id))

        if not memo_cbk:
            # Update the memoizer with the new result if this is not a
            # result from a memo lookup and the task has reached a terminal state.
            self.memoizer.update_memo(task_id, self.tasks[task_id], future)

            if self.checkpoint_mode == 'task_exit':
                self.checkpoint(tasks=[task_id])

        # Submit _*_stage_out tasks for output data futures that correspond with remote files
        if (self.tasks[task_id]['app_fu'] and
            self.tasks[task_id]['app_fu'].done() and
            self.tasks[task_id]['app_fu'].exception() is None and
            self.tasks[task_id]['executor'] != 'data_manager' and
            self.tasks[task_id]['func_name'] != '_ftp_stage_in' and
            self.tasks[task_id]['func_name'] != '_http_stage_in'):
            for dfu in self.tasks[task_id]['app_fu'].outputs:
                f = dfu.file_obj
                if isinstance(f, File) and f.is_remote():
                    self.data_manager.stage_out(f, self.tasks[task_id]['executor'])

        return