def Update(self, filename, clean_lines, linenum, error):
    """Update nesting state with current line.

    Args:
      filename: The name of the current file.
      clean_lines: A CleansedLines instance containing the file.
      linenum: The number of the line to check.
      error: The function to call with any errors found.
    """
    line = clean_lines.elided[linenum]

    # Remember top of the previous nesting stack.
    #
    # The stack is always pushed/popped and not modified in place, so
    # we can just do a shallow copy instead of copy.deepcopy.  Using
    # deepcopy would slow down cpplint by ~28%.
    if self.stack:
      self.previous_stack_top = self.stack[-1]
    else:
      self.previous_stack_top = None

    # Update pp_stack
    self.UpdatePreprocessor(line)

    # Count parentheses.  This is to avoid adding struct arguments to
    # the nesting stack.
    if self.stack:
      inner_block = self.stack[-1]
      depth_change = line.count('(') - line.count(')')
      inner_block.open_parentheses += depth_change

      # Also check if we are starting or ending an inline assembly block.
      if inner_block.inline_asm in (_NO_ASM, _END_ASM):
        if (depth_change != 0 and
            inner_block.open_parentheses == 1 and
            _MATCH_ASM.match(line)):
          # Enter assembly block
          inner_block.inline_asm = _INSIDE_ASM
        else:
          # Not entering assembly block.  If previous line was _END_ASM,
          # we will now shift to _NO_ASM state.
          inner_block.inline_asm = _NO_ASM
      elif (inner_block.inline_asm == _INSIDE_ASM and
            inner_block.open_parentheses == 0):
        # Exit assembly block
        inner_block.inline_asm = _END_ASM

    # Consume namespace declaration at the beginning of the line.  Do
    # this in a loop so that we catch same line declarations like this:
    #   namespace proto2 { namespace bridge { class MessageSet; } }
    while True:
      # Match start of namespace.  The "\b\s*" below catches namespace
      # declarations even if it weren't followed by a whitespace, this
      # is so that we don't confuse our namespace checker.  The
      # missing spaces will be flagged by CheckSpacing.
      namespace_decl_match = Match(r'^\s*namespace\b\s*([:\w]+)?(.*)$', line)
      if not namespace_decl_match:
        break

      new_namespace = _NamespaceInfo(namespace_decl_match.group(1), linenum)
      self.stack.append(new_namespace)

      line = namespace_decl_match.group(2)
      if line.find('{') != -1:
        new_namespace.seen_open_brace = True
        line = line[line.find('{') + 1:]

    # Look for a class declaration in whatever is left of the line
    # after parsing namespaces.  The regexp accounts for decorated classes
    # such as in:
    #   class LOCKABLE API Object {
    #   };
    class_decl_match = Match(
        r'^(\s*(?:template\s*<[\w\s<>,:=]*>\s*)?'
        r'(class|struct)\s+(?:[A-Z_]+\s+)*(\w+(?:::\w+)*))'
        r'(.*)$', line)
    if (class_decl_match and
        (not self.stack or self.stack[-1].open_parentheses == 0)):
      # We do not want to accept classes that are actually template arguments:
      #   template <class Ignore1,
      #             class Ignore2 = Default<Args>,
      #             template <Args> class Ignore3>
      #   void Function() {};
      #
      # To avoid template argument cases, we scan forward and look for
      # an unmatched '>'.  If we see one, assume we are inside a
      # template argument list.
      end_declaration = len(class_decl_match.group(1))
      if not self.InTemplateArgumentList(clean_lines, linenum, end_declaration):
        self.stack.append(_ClassInfo(
            class_decl_match.group(3), class_decl_match.group(2),
            clean_lines, linenum))
        line = class_decl_match.group(4)

    # If we have not yet seen the opening brace for the innermost block,
    # run checks here.
    if not self.SeenOpenBrace():
      self.stack[-1].CheckBegin(filename, clean_lines, linenum, error)

    # Update access control if we are inside a class/struct
    if self.stack and isinstance(self.stack[-1], _ClassInfo):
      classinfo = self.stack[-1]
      access_match = Match(
          r'^(.*)\b(public|private|protected|signals)(\s+(?:slots\s*)?)?'
          r':(?:[^:]|$)',
          line)
      if access_match:
        classinfo.access = access_match.group(2)

        # Check that access keywords are indented +1 space.  Skip this
        # check if the keywords are not preceded by whitespaces.
        indent = access_match.group(1)
        if (len(indent) != classinfo.class_indent + 1 and
            Match(r'^\s*$', indent)):
          if classinfo.is_struct:
            parent = 'struct ' + classinfo.name
          else:
            parent = 'class ' + classinfo.name
          slots = ''
          if access_match.group(3):
            slots = access_match.group(3)
          error(filename, linenum, 'whitespace/indent', 3,
                '%s%s: should be indented +1 space inside %s' % (
                    access_match.group(2), slots, parent))

    # Consume braces or semicolons from what's left of the line
    while True:
      # Match first brace, semicolon, or closed parenthesis.
      matched = Match(r'^[^{;)}]*([{;)}])(.*)$', line)
      if not matched:
        break

      token = matched.group(1)
      if token == '{':
        # If namespace or class hasn't seen a opening brace yet, mark
        # namespace/class head as complete.  Push a new block onto the
        # stack otherwise.
        if not self.SeenOpenBrace():
          self.stack[-1].seen_open_brace = True
        elif Match(r'^extern\s*"[^"]*"\s*\{', line):
          self.stack.append(_ExternCInfo(linenum))
        else:
          self.stack.append(_BlockInfo(linenum, True))
          if _MATCH_ASM.match(line):
            self.stack[-1].inline_asm = _BLOCK_ASM

      elif token == ';' or token == ')':
        # If we haven't seen an opening brace yet, but we already saw
        # a semicolon, this is probably a forward declaration.  Pop
        # the stack for these.
        #
        # Similarly, if we haven't seen an opening brace yet, but we
        # already saw a closing parenthesis, then these are probably
        # function arguments with extra "class" or "struct" keywords.
        # Also pop these stack for these.
        if not self.SeenOpenBrace():
          self.stack.pop()
      else:  # token == '}'
        # Perform end of block checks and pop the stack.
        if self.stack:
          self.stack[-1].CheckEnd(filename, clean_lines, linenum, error)
          self.stack.pop()
      line = matched.group(2)