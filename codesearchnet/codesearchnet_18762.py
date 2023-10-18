def update_experiments(self):
        """Experiment mapping."""
        # 693 Remove if 'not applicable'
        for field in record_get_field_instances(self.record, '693'):
            subs = field_get_subfields(field)
            all_subs = subs.get('a', []) + subs.get('e', [])
            if 'not applicable' in [x.lower() for x in all_subs]:
                record_delete_field(self.record, '693',
                                    field_position_global=field[4])
            new_subs = []
            experiment_a = ""
            experiment_e = ""
            for (key, value) in subs.iteritems():
                if key == 'a':
                    experiment_a = value[0]
                    new_subs.append((key, value[0]))
                elif key == 'e':
                    experiment_e = value[0]
            experiment = "%s---%s" % (experiment_a.replace(" ", "-"),
                                      experiment_e)
            translated_experiments = self.get_config_item(experiment,
                                                          "experiments")
            new_subs.append(("e", translated_experiments))
            record_delete_field(self.record, tag="693",
                                field_position_global=field[4])
            record_add_field(self.record, "693", subfields=new_subs)