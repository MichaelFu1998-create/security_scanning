def get_component_funcs(self, components=None):
        """
        Calculates the components functions that need to be executed for a deployment.
        """

        current_tp = self.get_current_thumbprint(components=components) or {}
        previous_tp = self.get_previous_thumbprint(components=components) or {}

        if self.verbose:
            print('Current thumbprint:')
            pprint(current_tp, indent=4)
            print('Previous thumbprint:')
            pprint(previous_tp, indent=4)

        differences = list(iter_dict_differences(current_tp, previous_tp))
        if self.verbose:
            print('Differences:')
            pprint(differences, indent=4)
        component_order = get_component_order([k for k, (_, _) in differences])
        if self.verbose:
            print('component_order:')
            pprint(component_order, indent=4)
        plan_funcs = list(get_deploy_funcs(component_order, current_tp, previous_tp))

        return component_order, plan_funcs