def update_experiments(self):
        """Experiment mapping."""
        # 693 Remove if 'not applicable'
        for field in record_get_field_instances(self.record, '693'):
            subs = field_get_subfields(field)
            acc_experiment = subs.get("e", [])
            if not acc_experiment:
                acc_experiment = subs.get("a", [])
                if not acc_experiment:
                    continue
            experiment = acc_experiment[-1]

            # Handle special case of leading experiments numbers NA-050 -> NA 50
            e_suffix = ""
            if "-NA-" in experiment or \
               "-RD-" in experiment or \
               "-WA-" in experiment:
                splitted_experiment = experiment.split("-")
                e_suffix = "-".join(splitted_experiment[2:])
                if e_suffix.startswith("0"):
                    e_suffix = e_suffix[1:]
                experiment = "-".join(splitted_experiment[:2])  # only CERN-NA

            translated_experiment = self.get_config_item(experiment,
                                                         "experiments")
            if not translated_experiment:
                continue
            new_subs = []
            if "---" in translated_experiment:
                experiment_a, experiment_e = translated_experiment.split("---")
                new_subs.append(("a", experiment_a.replace("-", " ")))
            else:
                experiment_e = translated_experiment
            new_subs.append(("e", experiment_e.replace("-", " ") + e_suffix))
            record_delete_field(self.record, tag="693",
                                field_position_global=field[4])
            record_add_field(self.record, "693", subfields=new_subs)