def random_word(length,dictionary = False):#may return offensive words if dictionary = True
    '''
    Creates random lowercase words from dictionary or by alternating vowels and consonants
    
    The second method chooses from 85**length words.
    The dictionary method chooses from 3000--12000 words for 3<=length<=12
    (though this of course depends on the available dictionary)
    
    :param length: word length
    :param dictionary: Try reading from dictionary, else fall back to artificial words
    '''
    if dictionary:
        try:
            with open('/usr/share/dict/words') as fp:
                words = [word.lower()[:-1] for word in fp.readlines() if re.match('[A-Za-z0-9]{}$'.format('{'+str(length)+'}'),word)]
            return random.choice(words)
        except FileNotFoundError:
            pass
    vowels = list('aeiou')
    consonants = list('bcdfghklmnprstvwz')
    pairs = [(random.choice(consonants),random.choice(vowels)) for _ in range(length//2+1)] 
    return ''.join([l for p in pairs for l in p])[:length]