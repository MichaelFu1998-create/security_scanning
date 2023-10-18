def _equivalent(self, char, prev, next, implicitA):
        """ Transliterate a Latin character equivalent to Devanagari.
        
        Add VIRAMA for ligatures.
        Convert standalone to dependent vowels.
        
        """
        result = []
        if char.isVowel == False:
            result.append(char.chr)
            if char.isConsonant \
            and ((next is not None and next.isConsonant) \
            or next is None): 
                result.append(DevanagariCharacter._VIRAMA)
        else:
            if prev is None or prev.isConsonant == False:
                result.append(char.chr)
            else:
                if char._dependentVowel is not None:
                    result.append(char._dependentVowel)
        return result