def spell_correct(string):
    """
    Uses aspell to spell correct an input string.
    Requires aspell to be installed and added to the path.
    Returns the spell corrected string if aspell is found, original string if not.
    string - string
    """

    # Create a temp file so that aspell could be used
    # By default, tempfile will delete this file when the file handle is closed.
    f = tempfile.NamedTemporaryFile(mode='w')
    f.write(string)
    f.flush()
    f_path = os.path.abspath(f.name)
    try:
        p = os.popen(aspell_path + " -a < " + f_path + " --sug-mode=ultra")

        # Aspell returns a list of incorrect words with the above flags
        incorrect = p.readlines()
        p.close()

    except Exception:
        log.exception("aspell process failed; could not spell check")
        # Return original string if aspell fails
        return string,0, string

    finally:
        f.close()

    incorrect_words = list()
    correct_spelling = list()
    for i in range(1, len(incorrect)):
        if(len(incorrect[i]) > 10):
            #Reformat aspell output to make sense
            match = re.search(":", incorrect[i])
            if hasattr(match, "start"):
                begstring = incorrect[i][2:match.start()]
                begmatch = re.search(" ", begstring)
                begword = begstring[0:begmatch.start()]

                sugstring = incorrect[i][match.start() + 2:]
                sugmatch = re.search(",", sugstring)
                if hasattr(sugmatch, "start"):
                    sug = sugstring[0:sugmatch.start()]

                    incorrect_words.append(begword)
                    correct_spelling.append(sug)

    #Create markup based on spelling errors
    newstring = string
    markup_string = string
    already_subbed=[]
    for i in range(0, len(incorrect_words)):
        sub_pat = r"\b" + incorrect_words[i] + r"\b"
        sub_comp = re.compile(sub_pat)
        newstring = re.sub(sub_comp, correct_spelling[i], newstring)
        if incorrect_words[i] not in already_subbed:
            markup_string=re.sub(sub_comp,'<bs>' + incorrect_words[i] + "</bs>", markup_string)
            already_subbed.append(incorrect_words[i])

    return newstring,len(incorrect_words),markup_string