def savedata(self, output, location=None):
        '''
        Save output data from any task in this workflow to S3

        Args:
               output: Reference task output (e.g. task.outputs.output1).

               location (optional): Subfolder under which the output will be saved.
                                    It will be placed under the account directory in gbd-customer-data bucket:
                                    s3://gbd-customer-data/{account_id}/{location}
                                    Leave blank to save to: workflow_output/{workflow_id}/{task_name}/{port_name}

        Returns:
            None
        '''

        output.persist = True
        if location:
            output.persist_location = location