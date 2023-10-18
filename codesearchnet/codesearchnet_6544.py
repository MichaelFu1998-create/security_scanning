def reindex_all(self, batch_size=1000):
        """
        Reindex all the records.

        By default, this method use Model.objects.all() but you can implement
        a method `get_queryset` in your subclass. This can be used to optimize
        the performance (for example with select_related or prefetch_related).
        """
        should_keep_synonyms = False
        should_keep_rules = False
        try:
            if not self.settings:
                self.settings = self.get_settings()
                logger.debug('Got settings for index %s: %s', self.index_name, self.settings)
            else:
                logger.debug("index %s already has settings: %s", self.index_name, self.settings)
        except AlgoliaException as e:
            if any("Index does not exist" in arg for arg in e.args):
                pass  # Expected, let's clear and recreate from scratch
            else:
                raise e  # Unexpected error while getting settings
        try:
            if self.settings:
                replicas = self.settings.get('replicas', None)
                slaves = self.settings.get('slaves', None)

                should_keep_replicas = replicas is not None
                should_keep_slaves = slaves is not None

                if should_keep_replicas:
                    self.settings['replicas'] = []
                    logger.debug("REMOVE REPLICAS FROM SETTINGS")
                if should_keep_slaves:
                    self.settings['slaves'] = []
                    logger.debug("REMOVE SLAVES FROM SETTINGS")

                self.__tmp_index.wait_task(self.__tmp_index.set_settings(self.settings)['taskID'])
                logger.debug('APPLY SETTINGS ON %s_tmp', self.index_name)
            rules = []
            synonyms = []
            for r in self.__index.iter_rules():
                rules.append(r)
            for s in self.__index.iter_synonyms():
                synonyms.append(s)
            if len(rules):
                logger.debug('Got rules for index %s: %s', self.index_name, rules)
                should_keep_rules = True
            if len(synonyms):
                logger.debug('Got synonyms for index %s: %s', self.index_name, rules)
                should_keep_synonyms = True

            self.__tmp_index.clear_index()
            logger.debug('CLEAR INDEX %s_tmp', self.index_name)

            counts = 0
            batch = []

            if hasattr(self, 'get_queryset'):
                qs = self.get_queryset()
            else:
                qs = self.model.objects.all()

            for instance in qs:
                if not self._should_index(instance):
                    continue  # should not index

                batch.append(self.get_raw_record(instance))
                if len(batch) >= batch_size:
                    self.__tmp_index.save_objects(batch)
                    logger.info('SAVE %d OBJECTS TO %s_tmp', len(batch),
                                self.index_name)
                    batch = []
                counts += 1
            if len(batch) > 0:
                self.__tmp_index.save_objects(batch)
                logger.info('SAVE %d OBJECTS TO %s_tmp', len(batch),
                            self.index_name)

            self.__client.move_index(self.__tmp_index.index_name,
                                     self.__index.index_name)
            logger.info('MOVE INDEX %s_tmp TO %s', self.index_name,
                        self.index_name)

            if self.settings:
                if should_keep_replicas:
                    self.settings['replicas'] = replicas
                    logger.debug("RESTORE REPLICAS")
                if should_keep_slaves:
                    self.settings['slaves'] = slaves
                    logger.debug("RESTORE SLAVES")
                if should_keep_replicas or should_keep_slaves:
                    self.__index.set_settings(self.settings)
                if should_keep_rules:
                    response = self.__index.batch_rules(rules, forward_to_replicas=True)
                    self.__index.wait_task(response['taskID'])
                    logger.info("Saved rules for index %s with response: {}".format(response), self.index_name)
                if should_keep_synonyms:
                    response = self.__index.batch_synonyms(synonyms, forward_to_replicas=True)
                    self.__index.wait_task(response['taskID'])
                    logger.info("Saved synonyms for index %s with response: {}".format(response), self.index_name)
            return counts
        except AlgoliaException as e:
            if DEBUG:
                raise e
            else:
                logger.warning('ERROR DURING REINDEXING %s: %s', self.model,
                               e)