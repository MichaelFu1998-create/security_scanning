def find_word_end(text, count=1):
        """ This is a helper method for self.expand_words().
            Finds the index of word endings (default is first word).
            The last word doesn't count.
            If there are no words, or there are no spaces in the word, it
            returns -1.

            This method ignores escape codes.
            Example:
                s = 'this is a test'
                i = find_word_end(s, count=1)
                print('-'.join((s[:i], s[i:])))
                # 'this- is a test'
                i = find_word_end(s, count=2)
                print('-'.join((s[:i], s[i:])))
                # 'this is- a test'
        """
        if not text:
            return -1
        elif ' ' not in text:
            return 0
        elif not text.strip():
            return -1
        count = count or 1
        found = 0
        foundindex = -1
        inword = False
        indices = get_indices(str(text))
        sortedindices = sorted(indices)
        for i in sortedindices:
            c = indices[i]
            if inword and c.isspace():
                # Found space.
                inword = False
                foundindex = i
                found += 1
                # Was there an escape code before this space?
                testindex = i
                while testindex > 0:
                    testindex -= 1
                    s = indices.get(testindex, None)
                    if s is None:
                        # Must be in the middle of an escape code.
                        continue
                    if len(s) == 1:
                        # Test index was a char.
                        foundindex = testindex + 1
                        break

                if found == count:
                    return foundindex
            elif not c.isspace():
                inword = True
        # We ended in a word/escape-code, or there were no words.
        lastindex = sortedindices[-1]
        if len(indices[lastindex]) > 1:
            # Last word included an escape code. Rewind a bit.
            while lastindex > 0:
                lastindex -= 1
                s = indices.get(lastindex, None)
                if s is None:
                    # Must be in the middle of an escape code.
                    continue
                if len(s) == 1:
                    # Found last char.
                    return lastindex + 1

        return -1 if inword else foundindex