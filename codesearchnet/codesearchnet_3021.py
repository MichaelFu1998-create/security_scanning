def UpdatePreprocessor(self, line):
    """Update preprocessor stack.

    We need to handle preprocessors due to classes like this:
      #ifdef SWIG
      struct ResultDetailsPageElementExtensionPoint {
      #else
      struct ResultDetailsPageElementExtensionPoint : public Extension {
      #endif

    We make the following assumptions (good enough for most files):
    - Preprocessor condition evaluates to true from #if up to first
      #else/#elif/#endif.

    - Preprocessor condition evaluates to false from #else/#elif up
      to #endif.  We still perform lint checks on these lines, but
      these do not affect nesting stack.

    Args:
      line: current line to check.
    """
    if Match(r'^\s*#\s*(if|ifdef|ifndef)\b', line):
      # Beginning of #if block, save the nesting stack here.  The saved
      # stack will allow us to restore the parsing state in the #else case.
      self.pp_stack.append(_PreprocessorInfo(copy.deepcopy(self.stack)))
    elif Match(r'^\s*#\s*(else|elif)\b', line):
      # Beginning of #else block
      if self.pp_stack:
        if not self.pp_stack[-1].seen_else:
          # This is the first #else or #elif block.  Remember the
          # whole nesting stack up to this point.  This is what we
          # keep after the #endif.
          self.pp_stack[-1].seen_else = True
          self.pp_stack[-1].stack_before_else = copy.deepcopy(self.stack)

        # Restore the stack to how it was before the #if
        self.stack = copy.deepcopy(self.pp_stack[-1].stack_before_if)
      else:
        # TODO(unknown): unexpected #else, issue warning?
        pass
    elif Match(r'^\s*#\s*endif\b', line):
      # End of #if or #else blocks.
      if self.pp_stack:
        # If we saw an #else, we will need to restore the nesting
        # stack to its former state before the #else, otherwise we
        # will just continue from where we left off.
        if self.pp_stack[-1].seen_else:
          # Here we can just use a shallow copy since we are the last
          # reference to it.
          self.stack = self.pp_stack[-1].stack_before_else
        # Drop the corresponding #if
        self.pp_stack.pop()
      else:
        # TODO(unknown): unexpected #endif, issue warning?
        pass