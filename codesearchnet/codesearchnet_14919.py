def _substituteCheckPattern(self, inputString, lineNumber, lastLineNumber, checkFileName, isForRegex):
        """
        Do various ${} substitutions
        """
        assert isinstance(inputString, str)
        assert isinstance(lineNumber, int)
        assert isinstance(lastLineNumber, int)
        assert isinstance(checkFileName, str)

        """
        Do ${LINE}, ${LINE:+N}, and ${LINE:-N} substitutions.
        To escape prepend with slash
        """
        sPattern = r'\$\{LINE(\:(?P<sign>\+|-)(?P<offset>\d+))?\}'
        matcher = re.compile(sPattern)
        result = ""
        loop = True
        start = 0
        end = len(inputString) # Not inclusive
        while loop:
            m = matcher.search(inputString, start, end)
            if not m:
                # No match so copy verbatim
                _logger.debug('Result is currently "{}"'.format(result))
                result += inputString[start:end]
                break # And we're done :)
            else:
                prevIndex = max(0, m.start() -1)
                _logger.debug('Previous character before match is at index {index} "{char}"'.format(index=prevIndex, char=inputString[prevIndex]))
                if inputString[prevIndex] == "\\":
                    # User asked to escape
                    _logger.debug('Substitution is escaped')
                    _logger.debug('Result is currently "{}"'.format(result))
                    result += inputString[start:prevIndex] # Copy before escaping character
                    _logger.debug('Result is currently "{}"'.format(result))
                    result += inputString[(prevIndex+1):m.end()] # Copy the ${LINE..} verbatim
                    start = min(m.end(), end)
                    _logger.debug('Result is currently "{}"'.format(result))
                    _logger.debug('Next search is {start}:{end} = "{ss}"'.format(start=start, end=end, ss=inputString[start:end]))
                else:
                    _logger.debug('Result is currently "{}"'.format(result))
                    _logger.debug('Doing subsitution. Found at {begin}:{end} = {ss}'.format(begin=m.start(),end=m.end(), ss=inputString[m.start():m.end()]))
                    result += inputString[start:m.start()] # Copy before substitution starts

                    if m.groupdict()['sign'] == None:
                        # No offset just substitute line number
                        _logger.debug('No offset')
                        result += str(lineNumber)
                    else:
                        offset = 1 if m.groupdict()['sign'] == '+' else -1
                        offset *= int(m.groupdict()['offset'])
                        _logger.debug('Offset is {}'.format(offset))

                        requestedLineNumber = lineNumber + offset
                        _logger.debug('Request line number to print is  {}'.format(requestedLineNumber))

                        if requestedLineNumber <= 0:
                            raise ParsingException('{file}:{line}:{col} offset gives line number < 1'.format(file=checkFileName, line=lineNumber, col=m.start()))
                        elif requestedLineNumber > lastLineNumber:
                            raise ParsingException('{file}:{line}:{col} offset gives line number past the end of file'.format(file=checkFileName, line=lineNumber, col=m.start()))

                        result += str(requestedLineNumber)

                    start = min(m.end(),end)
                    _logger.debug('Next search is {start}:{end} = "{ss}"'.format(start=start, end=end, ss=inputString[start:end]))

        """
        Do simple ${...} substitutions
        """


        # Do ${CHECKFILE_NAME} substitution
        basenameCheckFileName = os.path.basename(checkFileName)
        assert basenameCheckFileName.count('\\') == 0
        result = self._simpleSubstitution("CHECKFILE_NAME", basenameCheckFileName, result)

        # Do ${CHECKFILE_ABS_PATH} substitution
        abspathCheckFileName = os.path.abspath(checkFileName)
        if isForRegex:
            # Note slash substitution is for Windows paths (e.g. "c:\mything\foo.txt") which can break regexes if we don't
            # correctly escape them.
            abspathCheckFileName = abspathCheckFileName.replace('\\', '\\\\')

        result = self._simpleSubstitution("CHECKFILE_ABS_PATH", abspathCheckFileName, result)

        assert len(result) != 0
        return result