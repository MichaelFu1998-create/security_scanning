def get_siblings_content(self, current_sibling, baselinescore_siblings_para):
        """
        adds any siblings that may have a decent score to this node
        """
        if current_sibling.tag == 'p' and self.parser.getText(current_sibling):
            tmp = current_sibling
            if tmp.tail:
                tmp = deepcopy(tmp)
                tmp.tail = ''
            return [tmp]
        else:
            potential_paragraphs = self.parser.getElementsByTag(current_sibling, tag='p')
            if potential_paragraphs is None:
                return None

            paragraphs = list()
            for first_paragraph in potential_paragraphs:
                text = self.parser.getText(first_paragraph)
                if text:  # no len(text) > 0
                    word_stats = self.stopwords_class(language=self.get_language()).get_stopword_count(text)
                    paragraph_score = word_stats.get_stopword_count()
                    sibling_baseline_score = float(.30)
                    high_link_density = self.is_highlink_density(first_paragraph)
                    score = float(baselinescore_siblings_para * sibling_baseline_score)
                    if score < paragraph_score and not high_link_density:
                        para = self.parser.createElement(tag='p', text=text, tail=None)
                        paragraphs.append(para)
            return paragraphs