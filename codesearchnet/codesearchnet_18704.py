def convert_html_subscripts_to_latex(text):
    """Convert some HTML tags to latex equivalents."""
    text = re.sub("<sub>(.*?)</sub>", r"$_{\1}$", text)
    text = re.sub("<sup>(.*?)</sup>", r"$^{\1}$", text)
    return text