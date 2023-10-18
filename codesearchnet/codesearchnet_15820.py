def generate_diff_html(self):
    """
    Generate the summary diff report html from template
    :return: generated html to be written to disk
    """
    if not os.path.exists(self.resource_directory):
      os.makedirs(self.resource_directory)
    self.copy_local_includes()
    div_html = ''
    for plot_div in sorted(self.plot_files):
      with open(plot_div, 'r') as div_file:
        div_html += '\n' + div_file.read()
    template_loader = FileSystemLoader(self.get_resources_location())
    template_environment = Environment(loader=template_loader)
    template_environment.filters['sanitize_string'] = naarad.utils.sanitize_string
    diff_html = template_environment.get_template(CONSTANTS.TEMPLATE_HEADER).render(custom_stylesheet_includes=CONSTANTS.STYLESHEET_INCLUDES,
                                                                                    custom_javascript_includes=CONSTANTS.JAVASCRIPT_INCLUDES,
                                                                                    resource_path=self.resource_path,
                                                                                    report_title='naarad diff report') + '\n'
    diff_html += template_environment.get_template(CONSTANTS.TEMPLATE_DIFF_PAGE).render(diff_data=self.diff_data, plot_div_content=div_html,
                                                                                        reports=self.reports, sla_failure_list=self.sla_failure_list,
                                                                                        sla_map=self.sla_map) + '\n'
    diff_html += template_environment.get_template(CONSTANTS.TEMPLATE_FOOTER).render()
    return diff_html