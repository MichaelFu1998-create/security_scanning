def __feed_arthur(self):
        """ Feed Ocean with backend data collected from arthur redis queue"""

        with self.ARTHUR_FEED_LOCK:

            # This is a expensive operation so don't do it always
            if (time.time() - self.ARTHUR_LAST_MEMORY_CHECK) > 5 * self.ARTHUR_LAST_MEMORY_CHECK_TIME:
                self.ARTHUR_LAST_MEMORY_CHECK = time.time()
                logger.debug("Measuring the memory used by the raw items dict ...")
                try:
                    memory_size = self.measure_memory(self.arthur_items) / (1024 * 1024)
                except RuntimeError as ex:
                    # During memory usage measure, other thread could change the dict
                    logger.warning("Can't get the memory used by the raw items dict: %s", ex)
                    memory_size = self.ARTHUR_LAST_MEMORY_SIZE
                self.ARTHUR_LAST_MEMORY_CHECK_TIME = time.time() - self.ARTHUR_LAST_MEMORY_CHECK
                logger.debug("Arthur items memory size: %0.2f MB (%is to check)",
                             memory_size, self.ARTHUR_LAST_MEMORY_CHECK_TIME)
                self.ARTHUR_LAST_MEMORY_SIZE = memory_size

            # Don't feed items from redis if the current python dict is
            # larger than ARTHUR_MAX_MEMORY_SIZE

            if self.ARTHUR_LAST_MEMORY_SIZE > self.ARTHUR_MAX_MEMORY_SIZE:
                logger.debug("Items queue full. Not collecting items from redis queue.")
                return

            logger.info("Collecting items from redis queue")

            db_url = self.config.get_conf()['es_collection']['redis_url']

            conn = redis.StrictRedis.from_url(db_url)
            logger.debug("Redis connection stablished with %s.", db_url)

            # Get and remove queued items in an atomic transaction
            pipe = conn.pipeline()
            # pipe.lrange(Q_STORAGE_ITEMS, 0, -1)
            pipe.lrange(Q_STORAGE_ITEMS, 0, self.ARTHUR_REDIS_ITEMS - 1)
            pipe.ltrim(Q_STORAGE_ITEMS, self.ARTHUR_REDIS_ITEMS, -1)
            items = pipe.execute()[0]

            for item in items:
                arthur_item = pickle.loads(item)
                if arthur_item['tag'] not in self.arthur_items:
                    self.arthur_items[arthur_item['tag']] = []
                self.arthur_items[arthur_item['tag']].append(arthur_item)

            for tag in self.arthur_items:
                if self.arthur_items[tag]:
                    logger.debug("Arthur items for %s: %i", tag, len(self.arthur_items[tag]))