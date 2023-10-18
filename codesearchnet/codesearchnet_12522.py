def ingest_vectors(self, output_port_value):
        ''' append two required tasks to the given output to ingest to VS
        '''
        # append two tasks to self['definition']['tasks']
        ingest_task = Task('IngestItemJsonToVectorServices')
        ingest_task.inputs.items = output_port_value
        ingest_task.impersonation_allowed = True

        stage_task = Task('StageDataToS3')
        stage_task.inputs.destination = 's3://{vector_ingest_bucket}/{recipe_id}/{run_id}/{task_name}'
        stage_task.inputs.data = ingest_task.outputs.result.value

        self.definition['tasks'].append(ingest_task.generate_task_workflow_json())
        self.definition['tasks'].append(stage_task.generate_task_workflow_json())