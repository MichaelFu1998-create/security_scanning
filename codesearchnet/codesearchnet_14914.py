def make_python_patterns(additional_keywords=[], additional_builtins=[]):
    """Strongly inspired from idlelib.ColorDelegator.make_pat"""
    kw = r"\b" + any("keyword", kwlist + additional_keywords) + r"\b"
    kw_namespace = r"\b" + any("namespace", kw_namespace_list) + r"\b"
    word_operators = r"\b" + any("operator_word", wordop_list) + r"\b"
    builtinlist = [str(name) for name in dir(builtins)
                   if not name.startswith('_')] + additional_builtins
    for v in ['None', 'True', 'False']:
        builtinlist.remove(v)
    builtin = r"([^.'\"\\#]\b|^)" + any("builtin", builtinlist) + r"\b"
    builtin_fct = any("builtin_fct", [r'_{2}[a-zA-Z_]*_{2}'])
    comment = any("comment", [r"#[^\n]*"])
    instance = any("instance", [r"\bself\b", r"\bcls\b"])
    decorator = any('decorator', [r'@\w*', r'.setter'])
    number = any("number",
                 [r"\b[+-]?[0-9]+[lLjJ]?\b",
                  r"\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b",
                  r"\b[+-]?0[oO][0-7]+[lL]?\b",
                  r"\b[+-]?0[bB][01]+[lL]?\b",
                  r"\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?[jJ]?\b"])
    sqstring = r"(\b[rRuU])?'[^'\\\n]*(\\.[^'\\\n]*)*'?"
    dqstring = r'(\b[rRuU])?"[^"\\\n]*(\\.[^"\\\n]*)*"?'
    uf_sqstring = r"(\b[rRuU])?'[^'\\\n]*(\\.[^'\\\n]*)*(\\)$(?!')$"
    uf_dqstring = r'(\b[rRuU])?"[^"\\\n]*(\\.[^"\\\n]*)*(\\)$(?!")$'
    sq3string = r"(\b[rRuU])?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
    dq3string = r'(\b[rRuU])?"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
    uf_sq3string = r"(\b[rRuU])?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(\\)?(?!''')$"
    uf_dq3string = r'(\b[rRuU])?"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(\\)?(?!""")$'
    string = any("string", [sq3string, dq3string, sqstring, dqstring])
    ufstring1 = any("uf_sqstring", [uf_sqstring])
    ufstring2 = any("uf_dqstring", [uf_dqstring])
    ufstring3 = any("uf_sq3string", [uf_sq3string])
    ufstring4 = any("uf_dq3string", [uf_dq3string])
    return "|".join([instance, decorator, kw, kw_namespace, builtin,
                     word_operators, builtin_fct, comment,
                     ufstring1, ufstring2, ufstring3, ufstring4, string,
                     number, any("SYNC", [r"\n"])])