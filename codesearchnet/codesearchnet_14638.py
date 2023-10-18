def from_config(
            cls, cfg,
            default_fg=DEFAULT_FG_16, default_bg=DEFAULT_BG_16,
            default_fg_hi=DEFAULT_FG_256, default_bg_hi=DEFAULT_BG_256,
            max_colors=2**24
    ):
        """
        Build a palette definition from either a simple string or a dictionary,
        filling in defaults for items not specified.

        e.g.:
            "dark green"
                dark green foreground, black background

            {lo: dark gray, hi: "#666"}
                dark gray on 16-color terminals, #666 for 256+ color

        """
        # TODO: mono

        e = PaletteEntry(mono = default_fg,
                         foreground=default_fg,
                         background=default_bg,
                         foreground_high=default_fg_hi,
                         background_high=default_bg_hi)

        if isinstance(cfg, str):
            e.foreground_high = cfg
            if e.allowed(cfg, 16):
                e.foreground = cfg
            else:
                rgb = AttrSpec(fg=cfg, bg="", colors=max_colors).get_rgb_values()[0:3]
                e.foreground = nearest_basic_color(rgb)

        elif isinstance(cfg, dict):

            bg = cfg.get("bg", None)
            if isinstance(bg, str):
                e.background_high = bg
                if e.allowed(bg, 16):
                    e.background = bg
                else:
                    rgb = AttrSpec(fg=bg, bg="", colors=max_colors).get_rgb_values()[0:3]
                    e.background = nearest_basic_color(rgb)
            elif isinstance(bg, dict):
                e.background_high = bg.get("hi", default_bg_hi)
                if "lo" in bg:
                    if e.allowed(bg["lo"], 16):
                        e.background = bg["lo"]
                    else:
                        rgb = AttrSpec(fg=bg["lo"], bg="", colors=max_colors).get_rgb_values()[0:3]
                        e.background = nearest_basic_color(rgb)

            fg = cfg.get("fg", cfg)
            if isinstance(fg, str):
                e.foreground_high = fg
                if e.allowed(fg, 16):
                    e.foreground = fg
                else:
                    rgb = AttrSpec(fg=fg, bg="", colors=max_colors).get_rgb_values()[0:3]
                    e.foreground = nearest_basic_color(rgb)

            elif isinstance(fg, dict):
                e.foreground_high = fg.get("hi", default_fg_hi)
                if "lo" in fg:
                    if e.allowed(fg["lo"], 16):
                        e.foreground = fg["lo"]
                    else:
                        rgb = AttrSpec(fg=fg["lo"], bg="", colors=max_colors).get_rgb_values()[0:3]
                        e.foreground = nearest_basic_color(rgb)
        return e