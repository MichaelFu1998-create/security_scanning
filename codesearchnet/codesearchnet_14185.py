def parse(self, light=False):

        """ Parses data from Wikipedia page markup.

        The markup comes from Wikipedia's edit page.
        We parse it here into objects containing plain text.
        The light version parses only links to other articles, it's faster than a full parse.    
        
        """

        markup = self.markup
        
        self.disambiguation = self.parse_disambiguation(markup)
        self.categories = self.parse_categories(markup)
        self.links = self.parse_links(markup)
        
        if not light:
        
            # Conversion of HTML markup to Wikipedia markup.
            markup = self.convert_pre(markup)
            markup = self.convert_li(markup)
            markup = self.convert_table(markup)
            markup = replace_entities(markup)
        
            # Harvest references from the markup
            # and replace them by footnotes.
            markup = markup.replace("{{Cite", "{{cite")
            markup = re.sub("\{\{ {1,2}cite", "{{cite", markup)
            self.references, markup = self.parse_references(markup)

            # Make sure there are no legend linebreaks in image links.
            # Then harvest images and strip them from the markup.
            markup = re.sub("\n+(\{\{legend)", "\\1", markup)
            self.images, markup = self.parse_images(markup)
            self.images.extend(self.parse_gallery_images(markup))
            
            self.paragraphs = self.parse_paragraphs(markup)
            self.tables = self.parse_tables(markup)
            self.translations = self.parse_translations(markup)
            self.important = self.parse_important(markup)