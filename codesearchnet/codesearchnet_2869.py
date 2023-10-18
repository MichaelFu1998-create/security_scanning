def _handle_assignment_message(self, pplan):
    """Called when new NewInstanceAssignmentMessage arrives"""
    Log.debug("In handle_assignment_message() of STStmgrClient, Physical Plan: \n%s", str(pplan))
    self.heron_instance_cls.handle_assignment_msg(pplan)