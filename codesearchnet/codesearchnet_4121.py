def sub_chars(string):
    """
    Strips illegal characters from a string.  Used to sanitize input essays.
    Removes all non-punctuation, digit, or letter characters.
    Returns sanitized string.
    string - string
    """
    #Define replacement patterns
    sub_pat = r"[^A-Za-z\.\?!,';:]"
    char_pat = r"\."
    com_pat = r","
    ques_pat = r"\?"
    excl_pat = r"!"
    sem_pat = r";"
    col_pat = r":"
    whitespace_pat = r"\s{1,}"

    #Replace text.  Ordering is very important!
    nstring = re.sub(sub_pat, " ", string)
    nstring = re.sub(char_pat," .", nstring)
    nstring = re.sub(com_pat, " ,", nstring)
    nstring = re.sub(ques_pat, " ?", nstring)
    nstring = re.sub(excl_pat, " !", nstring)
    nstring = re.sub(sem_pat, " ;", nstring)
    nstring = re.sub(col_pat, " :", nstring)
    nstring = re.sub(whitespace_pat, " ", nstring)

    return nstring