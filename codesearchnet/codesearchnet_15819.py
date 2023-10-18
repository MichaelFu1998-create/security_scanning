def generate_client_charting_page(self, data_sources):
    """
    Create the client charting page for the diff report, with time series data from the two diffed reports.
    :return: generated html to be written to disk
    """
    if not os.path.exists(self.resource_directory):
      os.makedirs(self.resource_directory)
    self.copy_local_includes()
    template_loader = FileSystemLoader(self.get_resources_location())
    template_environment = Environment(loader=template_loader)
    client_html = template_environment.get_template(CONSTANTS.TEMPLATE_HEADER).render(custom_stylesheet_includes=CONSTANTS.STYLESHEET_INCLUDES,
                                                                                      custom_javascript_includes=CONSTANTS.JAVASCRIPT_INCLUDES,
                                                                                      resource_path=self.resource_path,
                                                                                      report_title='naarad diff report') + '\n'
    client_html += template_environment.get_template(CONSTANTS.TEMPLATE_DIFF_CLIENT_CHARTING).render(data_series=data_sources,
                                                                                                     resource_path=self.resource_path) + '\n'
    client_html += template_environment.get_template(CONSTANTS.TEMPLATE_FOOTER).render()
    return client_html