def log_error(self, text: str) -> None:
        '''
        Given some error text it will log the text if self.log_errors is True

        :param text: Error text to log
        '''
        if self.log_errors:
            with self._log_fp.open('a+') as log_file:
                log_file.write(f'{text}\n')