def parse_references(self, markup):

        """ Returns a list of references found in the markup.
        
        References appear inline as <ref> footnotes, 
        http:// external links, or {{cite}} citations.
        We replace it with (1)-style footnotes.
        Additional references data is gathered in
        parse_paragraph_references() when we parse paragraphs.
        
        References can also appear in image descriptions,
        tables and taxoboxes, so they might not always pop up in a paragraph.
        
        The plain() method finally replaces (1) by [1].
        
        """
    
        references = []
        
        # A Wikipedia reference note looks like:
        # <ref>In 1946, [[ENIAC]] consumed an estimated 174 kW. 
        # By comparison, a typical personal computer may use around 400 W; 
        # over four hundred times less. {{Ref harvard|kempf1961|Kempf 1961|a}}</ref>
        m = re.findall(self.re["reference"], markup)
        for reference in m:
            reference = re.sub("<ref> {0,1}cite", "<ref>{{cite", reference)
            if not reference.strip().startswith("[http://") and \
               not re.search("\{\{cite", reference):
                r = WikipediaReference()
                r.note = self.plain(re.sub("</{0,1}ref.*?>", "", reference))
                if r.note != "":
                    references.append(r)
                    p = " "+self.ref+"("+str(len(references))+")"
                    markup = markup.replace(reference, p, 1)
            else:
                # References containing a citation or url 
                # are better handled by the next patterns.
                pass
        
        # A Wikipedia citation looks like:
        # {{cite journal
        # | last = Einstein 
        # | first = Albert
        # | authorlink = Albert Einstein
        # | title = Sidelights on Relativity (Geometry and Experience) 
        # | publisher = P. Dutton., Co 
        # | date = 1923}}
        m = re.findall(self.re["citation"], markup)
        for citation in m:
            c = citation.replace("\n", "")
            r = WikipediaReference()
            for key in r.__dict__.keys():
                value = re.search("\| {0,1}"+key+"(.*?)[\|}]", c)
                if value:
                    value = value.group(1)
                    value = value.replace("link", "")
                    value = value.strip().strip(" =[]")
                    value = self.plain(value)
                    setattr(r, key, value)
            if r.first != "" and r.last != "":
                r.author = r.first + " " + r.last
            references.append(r)
            p = " "+self.ref+"("+str(len(references))+")"
            markup = markup.replace(citation, p, 1)
        
        # A Wikipedia embedded url looks like:
        # [http://www.pbs.org/wnet/hawking/html/home.html ''Stephen Hawking's Universe'']
        m = re.findall(self.re["url"], markup)
        for url in m:
            r = WikipediaReference()
            i = url.find(" ")
            if i > 0:
                r.url = url[:i].strip()
                r.note = self.plain(url[i:])
            else:
                r.url = url.strip()
            references.append(r)
            p = r.note+" "+self.ref+"("+str(len(references))+")"
            markup = markup.replace("["+url+"]", p, 1)

        # Since we parsed all citations first and then all notes and urls,
        # the ordering will not be correct in the markup,
        # e.g. (1) (11) (12) (2) (3).
        sorted = []
        m = re.findall(self.ref+"\(([0-9]*)\)", markup)
        for i in m:
            sorted.append(references[int(i)-1])
            markup = markup.replace(
                self.ref+"("+i+")", 
                self.ref+"**("+str(len(sorted))+")"
                )
        markup = markup.replace(self.ref+"**", self.ref)
        for r in references:
            if r not in sorted:
                sorted.append(r)
        references = sorted

        return references, markup.strip()