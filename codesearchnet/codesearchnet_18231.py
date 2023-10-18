def start(self):
        """Initializes the bot, plugins, and everything."""
        self.bot_start_time = datetime.now()
        self.webserver = Webserver(self.config['webserver']['host'], self.config['webserver']['port'])
        self.plugins.load()
        self.plugins.load_state()
        self._find_event_handlers()
        self.sc = ThreadedSlackClient(self.config['slack_token'])

        self.always_send_dm = ['_unauthorized_']
        if 'always_send_dm' in self.config:
            self.always_send_dm.extend(map(lambda x: '!' + x, self.config['always_send_dm']))

        # Rocket is very noisy at debug
        logging.getLogger('Rocket.Errors.ThreadPool').setLevel(logging.INFO)

        self.is_setup = True
        if self.test_mode:
            self.metrics['startup_time'] = (datetime.now() - self.bot_start_time).total_seconds() * 1000.0