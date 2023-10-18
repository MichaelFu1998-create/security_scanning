def parse_balanced_image(self, markup):
        
        """ Corrects Wikipedia image markup.

        Images have a description inside their link markup that 
        can contain link markup itself, make sure the outer "[" and "]" brackets 
        delimiting the image are balanced correctly (e.g. no [[ ]] ]]).

        Called from parse_images().

        """

        opened = 0
        closed = 0
        for i in range(len(markup)):
            if markup[i] == "[": opened += 1
            if markup[i] == "]": closed += 1
            if opened == closed:
                return markup[:i+1]
                
        return markup