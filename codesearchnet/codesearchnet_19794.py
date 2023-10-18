def add_line_error(self, line_data, error_info, log_level=logging.ERROR):
        """Helper function to record and log an error message

        :param line_data: dict
        :param error_info: dict
        :param logger:
        :param log_level: int
        :return:
        """
        if not error_info: return
        try:
            line_data['line_errors'].append(error_info)
        except KeyError:
            line_data['line_errors'] = [error_info]
        except TypeError: # no line_data
            pass
        try:
            self.logger.log(log_level, Gff3.error_format.format(current_line_num=line_data['line_index'] + 1, error_type=error_info['error_type'], message=error_info['message'], line=line_data['line_raw'].rstrip()))
        except AttributeError: # no logger
            pass