def plain(self, markup):
        
        """ Strips Wikipedia markup from given text.
        
        This creates a "plain" version of the markup,
        stripping images and references and the like.
        Does some commonsense maintenance as well,
        like collapsing multiple spaces.
        If you specified full_strip=False for WikipediaPage instance,
        some markup is preserved as HTML (links, bold, italic).
        
        """
        
        # Strip bold and italic.
        if self.full_strip:
            markup = markup.replace("'''", "")
            markup = markup.replace("''", "")
        else:
            markup = re.sub("'''([^']*?)'''", "<b>\\1</b>", markup)
            markup = re.sub("''([^']*?)''", "<i>\\1</i>", markup)
        
        # Strip image gallery sections.
        markup = re.sub(self.re["gallery"], "", markup)
        
        # Strip tables.
        markup = re.sub(self.re["table"], "", markup)
        markup = markup.replace("||", "")
        markup = markup.replace("|}", "")
        
        # Strip links, keeping the display alias.
        # We'll strip the ending ]] later.
        if self.full_strip:
            markup = re.sub(r"\[\[[^\]]*?\|", "", markup)
        else:
            markup = re.sub(r"\[\[([^]|]*|)\]\]", '<a href="\\1">\\1</a>', markup)
            markup = re.sub(r"\[\[([^]|]*|)\|([^]]*)\]\]", '<a href="\\1">\\2</a>', markup)    

        # Strip translations, users, etc.
        markup = re.sub(self.re["translation"], "", markup)
        
        # This math TeX is not supported:
        markup = markup.replace("\displaytyle", "")
        markup = markup.replace("\textstyle", "")
        markup = markup.replace("\scriptstyle", "")
        markup = markup.replace("\scriptscriptstyle", "")
        
        # Before stripping [ and ] brackets,
        # make sure they are retained inside <math></math> equations.
        markup = re.sub("(<math>.*?)\[(.*?</math>)", "\\1MATH___OPEN\\2", markup)
        markup = re.sub("(<math>.*?)\](.*?</math>)", "\\1MATH___CLOSE\\2", markup)
        markup = markup.replace("[", "")
        markup = markup.replace("]", "")
        markup = markup.replace("MATH___OPEN", "[")
        markup = markup.replace("MATH___CLOSE", "]")
        
        # a) Strip references.
        # b) Strip <ref></ref> tags.
        # c) Strip <ref name="" /> tags.
        # d) Replace --REF--(12) by [12].
        # e) Remove space between [12] and trailing punctuation .,
        # f) Remove HTML comment <!-- -->
        # g) Keep the Latin Extended-B template: {{latinx| }}
        # h) Strip Middle-Earth references.
        # i) Keep quotes: {{quote| }}
        # j) Remove templates
        markup = re.sub(self.re["reference"], "", markup)                  # a
        markup = re.sub("</{0,1}ref.*?>", "", markup)                      # b
        markup = re.sub("<ref name=\".*?\" {0,1}/>", "", markup)           # c
        markup = re.sub(self.ref+"\(([0-9]*?)\)", "[\\1] ", markup)        # d
        markup = re.sub("\] ([,.\"\?\)])", "]\\1", markup)                 # e
        markup = re.sub(self.re["comment"], "", markup)                    # f
        markup = re.sub("\{\{latinx\|(.*?)\}\}", "\\1", markup)            # g
        markup = re.sub("\{\{ME-ref.*?\}\}", "", markup)                   # h
        markup = re.sub("\{\{quote\|(.*?)\}\}", "\"\\1\"", markup)         # i
        markup = re.sub(re.compile("\{\{.*?\}\}", re.DOTALL), "", markup)  # j
        markup = markup.replace("}}", "")
        
        # Collapse multiple spaces between words,
        # unless they appear in preformatted text.
        markup = re.sub("<br.*?/{0,1}>", " ", markup)
        markup = markup.split("\n")
        for i in range(len(markup)):
            if not markup[i].startswith(" "):
                markup[i] = re.sub(r"[ ]+", " ", markup[i])
        markup = "\n".join(markup)
        markup = markup.replace(" .", ".")
        
        # Strip all HTML except <math> tags.
        if self.full_strip:
            markup = strip_tags(markup, exclude=["math"], linebreaks=True)
        
        markup = markup.strip()
        return markup