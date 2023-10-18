def rst2md(text):
    """Converts the RST text from the examples docstrigs and comments
    into markdown text for the IPython notebooks"""

    top_heading = re.compile(r'^=+$\s^([\w\s-]+)^=+$', flags=re.M)
    text = re.sub(top_heading, r'# \1', text)

    math_eq = re.compile(r'^\.\. math::((?:.+)?(?:\n+^  .+)*)', flags=re.M)
    text = re.sub(math_eq,
                  lambda match: r'$${0}$$'.format(match.group(1).strip()),
                  text)
    inline_math = re.compile(r':math:`(.+)`')
    text = re.sub(inline_math, r'$\1$', text)

    return text