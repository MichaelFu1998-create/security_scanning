def extract_metric_name(self, metric_name):
    """
    Method to extract SAR metric names from the section given in the config. The SARMetric class assumes that
    the section name will contain the SAR types listed in self.supported_sar_types tuple

    :param str metric_name: Section name from the config
    :return: str which identifies what kind of SAR metric the section represents
    """
    for metric_type in self.supported_sar_types:
      if metric_type in metric_name:
        return metric_type
    logger.error('Section [%s] does not contain a valid metric type, using type: "SAR-generic". Naarad works better '
                 'if it knows the metric type. Valid SAR metric names are: %s', metric_name, self.supported_sar_types)
    return 'SAR-generic'