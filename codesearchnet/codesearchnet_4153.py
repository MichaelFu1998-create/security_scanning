def create_essay_set(text, score, prompt_string, generate_additional=True):
    """
    Creates an essay set from given data.
    Text should be a list of strings corresponding to essay text.
    Score should be a list of scores where score[n] corresponds to text[n]
    Prompt string is just a string containing the essay prompt.
    Generate_additional indicates whether to generate additional essays at the minimum score point or not.
    """
    x = EssaySet()
    for i in xrange(0, len(text)):
        x.add_essay(text[i], score[i])
        if score[i] == min(score) and generate_additional == True:
            x.generate_additional_essays(x._clean_text[len(x._clean_text) - 1], score[i])

    x.update_prompt(prompt_string)

    return x