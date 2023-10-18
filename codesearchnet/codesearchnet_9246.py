def start(self):
        """
        This method defines the workflow of SirMordred. So it calls to:
        - initialize the databases
        - execute the different phases for the first iteration
          (collection, identities, enrichment)
        - start the collection and enrichment in parallel by data source
        - start also the Sorting Hat merge
        """

        # logger.debug("Starting SirMordred engine ...")
        logger.info("")
        logger.info("----------------------------")
        logger.info("Starting SirMordred engine ...")
        logger.info("- - - - - - - - - - - - - - ")

        # check we have access to the needed ES
        if not self.check_es_access():
            print('Can not access Elasticsearch service. Exiting sirmordred ...')
            sys.exit(1)

        # If arthur is configured check that it is working
        if self.conf['es_collection']['arthur']:
            if not self.check_redis_access():
                print('Can not access redis service. Exiting sirmordred ...')
                sys.exit(1)
            if not self.check_arthur_access():
                print('Can not access arthur service. Exiting sirmordred ...')
                sys.exit(1)

        # If bestiary is configured check that it is working
        if self.conf['projects']['projects_url']:
            if not self.check_bestiary_access():
                print('Can not access bestiary service. Exiting sirmordred ...')
                sys.exit(1)

        # Initial round: panels and projects loading
        self.__execute_initial_load()

        # Tasks to be executed during updating process
        all_tasks_cls = []
        all_tasks_cls.append(TaskProjects)  # projects update is always needed
        if self.conf['phases']['collection']:
            if not self.conf['es_collection']['arthur']:
                all_tasks_cls.append(TaskRawDataCollection)
            else:
                all_tasks_cls.append(TaskRawDataArthurCollection)
        if self.conf['phases']['identities']:
            # load identities and orgs periodically for updates
            all_tasks_cls.append(TaskIdentitiesLoad)
            all_tasks_cls.append(TaskIdentitiesMerge)
            all_tasks_cls.append(TaskIdentitiesExport)
            # This is done in enrichement before doing the enrich
            # if self.conf['phases']['collection']:
            #     all_tasks_cls.append(TaskIdentitiesCollection)
        if self.conf['phases']['enrichment']:
            all_tasks_cls.append(TaskEnrich)
        if self.conf['phases']['track_items']:
            all_tasks_cls.append(TaskTrackItems)
        if self.conf['phases']['report']:
            all_tasks_cls.append(TaskReport)

        # this is the main loop, where the execution should spend
        # most of its time

        while True:

            if not all_tasks_cls:
                logger.warning("No tasks to execute.")
                break

            try:
                if not self.conf['general']['update']:
                    self.execute_batch_tasks(all_tasks_cls,
                                             self.conf['sortinghat']['sleep_for'],
                                             self.conf['general']['min_update_delay'])
                    self.execute_batch_tasks(all_tasks_cls,
                                             self.conf['sortinghat']['sleep_for'],
                                             self.conf['general']['min_update_delay'])
                    break
                else:
                    self.execute_nonstop_tasks(all_tasks_cls)

                # FIXME this point is never reached so despite the exception is
                # handled and the error is shown, the traceback is not printed

            except DataCollectionError as e:
                logger.error(str(e))
                var = traceback.format_exc()
                logger.error(var)

            except DataEnrichmentError as e:
                logger.error(str(e))
                var = traceback.format_exc()
                logger.error(var)

        logger.info("Finished SirMordred engine ...")