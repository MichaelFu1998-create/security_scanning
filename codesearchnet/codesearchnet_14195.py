def parse_paragraph_list(self, markup, indent="\t"):
        
        """ Formats bullets and numbering of Wikipedia lists.
        
        List items are marked by "*", "#" or ";" at the start of a line.
        We treat ";" the same as "*",
        and replace "#" with real numbering (e.g. "2.").
        Sublists (e.g. *** and ###) get indented by tabs.
        
        Called from parse_paragraphs() method.
        
        """

        def lastleft(ch, str):
            n = 0
            while n < len(str) and str[n] == ch: n += 1
            return n        

        tally = [1 for i in range(10)]
        chunks = markup.split("\n")
        for i in range(len(chunks)):
            if chunks[i].startswith("#"):
                j = min(lastleft("#", chunks[i]), len(tally)-1)
                chunks[i] = indent*(j-1) + str(tally[j])+". " + chunks[i][j:]
                chunks[i] = chunks[i].replace(".  ", ". ")
                tally[j] += 1
                # Reset the numbering of sublists.
                for k in range(j+1, len(tally)): 
                    tally[k] = 1
            if chunks[i].startswith(";"):
                chunks[i] = "*" + chunks[i][1:]
            if chunks[i].startswith("*"):
                j = lastleft("*", chunks[i])  
                chunks[i] = indent*(j-1) + "* " + chunks[i][j:]
                chunks[i] = chunks[i].replace("*  ", "* ")
        
        return "\n".join(chunks)