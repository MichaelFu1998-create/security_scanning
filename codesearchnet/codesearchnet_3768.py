def _workflow_node_structure(node_results):
        '''
        Takes the list results from the API in `node_results` and
        translates this data into a dictionary organized in a
        human-readable heirarchial structure
        '''
        # Build list address translation, and create backlink lists
        node_list_pos = {}
        for i, node_result in enumerate(node_results):
            for rel in ['success', 'failure', 'always']:
                node_result['{0}_backlinks'.format(rel)] = []
            node_list_pos[node_result['id']] = i

        # Populate backlink lists
        for node_result in node_results:
            for rel in ['success', 'failure', 'always']:
                for sub_node_id in node_result['{0}_nodes'.format(rel)]:
                    j = node_list_pos[sub_node_id]
                    node_results[j]['{0}_backlinks'.format(rel)].append(
                        node_result['id'])

        # Find the root nodes
        root_nodes = []
        for node_result in node_results:
            is_root = True
            for rel in ['success', 'failure', 'always']:
                if node_result['{0}_backlinks'.format(rel)] != []:
                    is_root = False
                    break
            if is_root:
                root_nodes.append(node_result['id'])

        # Create network dictionary recursively from root nodes
        def branch_schema(node_id):
            i = node_list_pos[node_id]
            node_dict = node_results[i]
            ret_dict = {"id": node_id}
            for fd in NODE_STANDARD_FIELDS:
                val = node_dict.get(fd, None)
                if val is not None:
                    if fd == 'unified_job_template':
                        job_type = node_dict['summary_fields'][
                            'unified_job_template']['unified_job_type']
                        ujt_key = JOB_TYPES[job_type]
                        ret_dict[ujt_key] = val
                    else:
                        ret_dict[fd] = val
            for rel in ['success', 'failure', 'always']:
                sub_node_id_list = node_dict['{0}_nodes'.format(rel)]
                if len(sub_node_id_list) == 0:
                    continue
                relationship_name = '{0}_nodes'.format(rel)
                ret_dict[relationship_name] = []
                for sub_node_id in sub_node_id_list:
                    ret_dict[relationship_name].append(
                        branch_schema(sub_node_id))
            return ret_dict

        schema_dict = []
        for root_node_id in root_nodes:
            schema_dict.append(branch_schema(root_node_id))
        return schema_dict