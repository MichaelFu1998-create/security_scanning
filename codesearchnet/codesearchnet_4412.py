def check_tracking_enabled(self):
        """By default tracking is enabled.

        If Test mode is set via env variable PARSL_TESTING, a test flag is set

        Tracking is disabled if :
            1. config["globals"]["usageTracking"] is set to False (Bool)
            2. Environment variable PARSL_TRACKING is set to false (case insensitive)

        """
        track = True   # By default we track usage
        test = False  # By default we are not in testing mode

        testvar = str(os.environ.get("PARSL_TESTING", 'None')).lower()
        if testvar == 'true':
            test = True

        if not self.config.usage_tracking:
            track = False

        envvar = str(os.environ.get("PARSL_TRACKING", True)).lower()
        if envvar == "false":
            track = False

        return test, track