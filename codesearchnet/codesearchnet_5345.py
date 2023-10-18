def add_bpmn_xml(self, bpmn, svg=None, filename=None):
        """
        Add the given lxml representation of the BPMN file to the parser's set.

        :param svg: Optionally, provide the text data for the SVG of the BPMN
          file
        :param filename: Optionally, provide the source filename.
        """
        xpath = xpath_eval(bpmn)

        processes = xpath('.//bpmn:process')
        for process in processes:
            process_parser = self.PROCESS_PARSER_CLASS(
                self, process, svg, filename=filename, doc_xpath=xpath)
            if process_parser.get_id() in self.process_parsers:
                raise ValidationException(
                    'Duplicate process ID', node=process, filename=filename)
            if process_parser.get_name() in self.process_parsers_by_name:
                raise ValidationException(
                    'Duplicate process name', node=process, filename=filename)
            self.process_parsers[process_parser.get_id()] = process_parser
            self.process_parsers_by_name[
                process_parser.get_name()] = process_parser