def strip(self, text, *args, **kwargs):
        """
        Try to maintain parity with what is extracted by extract since strip
        will most likely be used in conjunction with extract
        """
        if OEMBED_DEFAULT_PARSE_HTML:
            extracted = self.extract_oembeds_html(text, *args, **kwargs)
        else:
            extracted = self.extract_oembeds(text, *args, **kwargs)
        
        matches = [r['original_url'] for r in extracted]
        match_handler = lambda m: m.group() not in matches and m.group() or ''
        
        return re.sub(URL_RE, match_handler, text)