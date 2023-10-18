def parse_files(self, files=None, sections=None):
        """Parse configfiles. 
        files <list str>, <str> or None:
            What files to parse. None means use self.configfiles. New
            values override old ones. A string value will be interpreted
            as a list of one item.
        sections <list str>, <str> or None:
            Which sections to parse from the files. None means use
            self.sections. A string value will be interpreted as a list
            of one item. The [DEFAULT]
            section is always read, and it is read as if its contents were
            copied to the beginning of all other sections.
            
        """
        files = _list(files, self.configfiles)
        sections = _list(sections, self.sections)
        for file in files:
            parser = StrictConfigParser()
            parser.read(file)
            for section in sections:
                if not parser.has_section(section):
                    continue
                for unused in parser.unusedoptions(section):
                    if unused not in self.options and unused not in self.ignore: 
                        templ = "The option %r in section [%s] of file %s does not exist."
                        raise InvalidOption(unused, message=templ % (unused, section, file))
                for name in parser.options(section):          
                    if name in self.options:
                        if self.options[name].reserved:
                            templ = "The option %s in section [%s] of file %s is reserved for command line use."
                            raise ReservedOptionError(message=templ % (unused, section, file))
                        value = parser.get(section, name)
                        self.options[name].parsestr(value, name, '%s [%s]' % (file, section))