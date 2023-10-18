def parse(self):
    """
    Parse the Jmeter file and calculate key stats

    :return: status of the metric parse
    """
    file_status = True
    for infile in self.infile_list:
      file_status = file_status and naarad.utils.is_valid_file(infile)
      if not file_status:
        return False

    status = self.parse_xml_jtl(self.aggregation_granularity)
    gc.collect()
    return status