def __studies(self, retention_time):
        """ Execute the studies configured for the current backend """

        cfg = self.config.get_conf()
        if 'studies' not in cfg[self.backend_section] or not \
           cfg[self.backend_section]['studies']:
            logger.debug('No studies for %s' % self.backend_section)
            return

        studies = [study for study in cfg[self.backend_section]['studies'] if study.strip() != ""]
        if not studies:
            logger.debug('No studies for %s' % self.backend_section)
            return

        logger.debug("Executing studies for %s: %s" % (self.backend_section, studies))
        time.sleep(2)  # Wait so enrichment has finished in ES
        enrich_backend = self._get_enrich_backend()
        ocean_backend = self._get_ocean_backend(enrich_backend)

        active_studies = []
        all_studies = enrich_backend.studies
        all_studies_names = [study.__name__ for study in enrich_backend.studies]

        # Time to check that configured studies are valid
        logger.debug("All studies in %s: %s", self.backend_section, all_studies_names)
        logger.debug("Configured studies %s", studies)
        cfg_studies_types = [study.split(":")[0] for study in studies]
        if not set(cfg_studies_types).issubset(set(all_studies_names)):
            logger.error('Wrong studies names for %s: %s', self.backend_section, studies)
            raise RuntimeError('Wrong studies names ', self.backend_section, studies)

        for study in enrich_backend.studies:
            if study.__name__ in cfg_studies_types:
                active_studies.append(study)

        enrich_backend.studies = active_studies
        print("Executing for %s the studies %s" % (self.backend_section,
              [study for study in studies]))

        studies_args = self.__load_studies()

        do_studies(ocean_backend, enrich_backend, studies_args, retention_time=retention_time)
        # Return studies to its original value
        enrich_backend.studies = all_studies