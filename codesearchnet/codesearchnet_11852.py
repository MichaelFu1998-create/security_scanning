def preview(self, components=None, ask=0):
        """
        Inspects differences between the last deployment and the current code state.
        """

        ask = int(ask)

        self.init()

        component_order, plan_funcs = self.get_component_funcs(components=components)

        print('\n%i changes found for host %s.\n' % (len(component_order), self.genv.host_string))
        if component_order and plan_funcs:
            if self.verbose:
                print('These components have changed:\n')
                for component in sorted(component_order):
                    print((' '*4)+component)
            print('Deployment plan for host %s:\n' % self.genv.host_string)
            for func_name, _ in plan_funcs:
                print(success_str((' '*4)+func_name))
        if component_order:
            print()

        if ask and self.genv.host_string == self.genv.hosts[-1]:
            if component_order:
                if not raw_input('Begin deployment? [yn] ').strip().lower().startswith('y'):
                    sys.exit(0)
            else:
                sys.exit(0)