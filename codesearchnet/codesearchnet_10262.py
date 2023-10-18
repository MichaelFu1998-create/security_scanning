def post_cleanup(self):
        """\
        remove any divs that looks like non-content,
        clusters of links, or paras with no gusto
        """
        parse_tags = ['p']
        if self.config.parse_lists:
            parse_tags.extend(['ul', 'ol'])
        if self.config.parse_headers:
            parse_tags.extend(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        target_node = self.article.top_node
        node = self.add_siblings(target_node)
        for elm in self.parser.getChildren(node):
            e_tag = self.parser.getTag(elm)
            if e_tag not in parse_tags:
                if (self.is_highlink_density(elm) or self.is_table_and_no_para_exist(elm) or
                        not self.is_nodescore_threshold_met(node, elm)):
                    self.parser.remove(elm)
        return node