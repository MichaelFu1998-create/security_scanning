def _replace_words(replacements, string):
    """Replace words with corresponding values in replacements dict.

    Words must be separated by spaces or newlines.
    """
    output_lines = []
    for line in string.split('\n'):
        output_words = []
        for word in line.split(' '):
            new_word = replacements.get(word, word)
            output_words.append(new_word)
        output_lines.append(output_words)
    return '\n'.join(' '.join(output_words) for output_words in output_lines)