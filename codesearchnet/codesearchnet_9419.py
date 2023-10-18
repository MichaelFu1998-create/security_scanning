def create_config(cls, cfgfile, nick, twtfile, twturl, disclose_identity, add_news):
        """Create a new config file at the default location.

        :param str cfgfile: path to the config file
        :param str nick: nickname to use for own tweets
        :param str twtfile: path to the local twtxt file
        :param str twturl: URL to the remote twtxt file
        :param bool disclose_identity: if true the users id will be disclosed
        :param bool add_news: if true follow twtxt news feed
        """
        cfgfile_dir = os.path.dirname(cfgfile)
        if not os.path.exists(cfgfile_dir):
            os.makedirs(cfgfile_dir)

        cfg = configparser.ConfigParser()

        cfg.add_section("twtxt")
        cfg.set("twtxt", "nick", nick)
        cfg.set("twtxt", "twtfile", twtfile)
        cfg.set("twtxt", "twturl", twturl)
        cfg.set("twtxt", "disclose_identity", str(disclose_identity))
        cfg.set("twtxt", "character_limit", "140")
        cfg.set("twtxt", "character_warning", "140")

        cfg.add_section("following")
        if add_news:
            cfg.set("following", "twtxt", "https://buckket.org/twtxt_news.txt")

        conf = cls(cfgfile, cfg)
        conf.write_config()
        return conf