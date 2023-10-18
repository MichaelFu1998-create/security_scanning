def setup(self, app):  # noqa
        """Initialize the application."""
        super().setup(app)

        # Setup Database
        self.database.initialize(connect(self.cfg.connection, **self.cfg.connection_params))

        # Fix SQLite in-memory database
        if self.database.database == ':memory:':
            self.cfg.connection_manual = True

        if not self.cfg.migrations_enabled:
            return

        # Setup migration engine
        self.router = Router(self.database, migrate_dir=self.cfg.migrations_path)

        # Register migration commands
        def pw_migrate(name: str=None, fake: bool=False):
            """Run application's migrations.

            :param name: Choose a migration' name
            :param fake: Run as fake. Update migration history and don't touch the database
            """
            self.router.run(name, fake=fake)

        self.app.manage.command(pw_migrate)

        def pw_rollback(name: str=None):
            """Rollback a migration.

            :param name: Migration name (actually it always should be a last one)
            """
            if not name:
                name = self.router.done[-1]
            self.router.rollback(name)

        self.app.manage.command(pw_rollback)

        def pw_create(name: str='auto', auto: bool=False):
            """Create a migration.

            :param name: Set name of migration [auto]
            :param auto: Track changes and setup migrations automatically
            """
            if auto:
                auto = list(self.models.values())
            self.router.create(name, auto)

        self.app.manage.command(pw_create)

        def pw_list():
            """List migrations."""
            self.router.logger.info('Migrations are done:')
            self.router.logger.info('\n'.join(self.router.done))
            self.router.logger.info('')
            self.router.logger.info('Migrations are undone:')
            self.router.logger.info('\n'.join(self.router.diff))

        self.app.manage.command(pw_list)

        @self.app.manage.command
        def pw_merge():
            """Merge migrations into one."""
            self.router.merge()

        self.app.manage.command(pw_merge)