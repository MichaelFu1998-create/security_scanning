def main():
    """Main entry point."""
    # Build default paths for files.
    dirs = appdirs.AppDirs('hangups', 'hangups')
    default_log_path = os.path.join(dirs.user_log_dir, 'hangups.log')
    default_token_path = os.path.join(dirs.user_cache_dir, 'refresh_token.txt')
    default_config_path = 'hangups.conf'
    user_config_path = os.path.join(dirs.user_config_dir, 'hangups.conf')

    # Create a default empty config file if does not exist.
    dir_maker(user_config_path)
    if not os.path.isfile(user_config_path):
        with open(user_config_path, 'a') as cfg:
            cfg.write("")

    parser = configargparse.ArgumentParser(
        prog='hangups', default_config_files=[default_config_path,
                                              user_config_path],
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
        add_help=False,  # Disable help so we can add it to the correct group.
    )
    general_group = parser.add_argument_group('General')
    general_group.add('-h', '--help', action='help',
                      help='show this help message and exit')
    general_group.add('--token-path', default=default_token_path,
                      help='path used to store OAuth refresh token')
    general_group.add('--date-format', default='< %y-%m-%d >',
                      help='date format string')
    general_group.add('--time-format', default='(%I:%M:%S %p)',
                      help='time format string')
    general_group.add('-c', '--config', help='configuration file path',
                      is_config_file=True, default=user_config_path)
    general_group.add('-v', '--version', action='version',
                      version='hangups {}'.format(hangups.__version__))
    general_group.add('-d', '--debug', action='store_true',
                      help='log detailed debugging messages')
    general_group.add('--manual-login', action='store_true',
                      help='enable manual login method')
    general_group.add('--log', default=default_log_path, help='log file path')
    key_group = parser.add_argument_group('Keybindings')
    key_group.add('--key-next-tab', default='ctrl d',
                  help='keybinding for next tab')
    key_group.add('--key-prev-tab', default='ctrl u',
                  help='keybinding for previous tab')
    key_group.add('--key-close-tab', default='ctrl w',
                  help='keybinding for close tab')
    key_group.add('--key-quit', default='ctrl e',
                  help='keybinding for quitting')
    key_group.add('--key-menu', default='ctrl n',
                  help='keybinding for context menu')
    key_group.add('--key-up', default='k',
                  help='keybinding for alternate up key')
    key_group.add('--key-down', default='j',
                  help='keybinding for alternate down key')
    key_group.add('--key-page-up', default='ctrl b',
                  help='keybinding for alternate page up')
    key_group.add('--key-page-down', default='ctrl f',
                  help='keybinding for alternate page down')
    notification_group = parser.add_argument_group('Notifications')
    # deprecated in favor of --notification-type=none:
    notification_group.add('-n', '--disable-notifications',
                           action='store_true',
                           help=configargparse.SUPPRESS)
    notification_group.add('-D', '--discreet-notifications',
                           action='store_true',
                           help='hide message details in notifications')
    notification_group.add('--notification-type',
                           choices=sorted(NOTIFIER_TYPES.keys()),
                           default='default',
                           help='type of notifications to create')

    # add color scheme options
    col_group = parser.add_argument_group('Colors')
    col_group.add('--col-scheme', choices=COL_SCHEMES.keys(),
                  default='default', help='colour scheme to use')
    col_group.add('--col-palette-colors', choices=('16', '88', '256'),
                  default=16, help='Amount of available colors')
    for name in COL_SCHEME_NAMES:
        col_group.add('--col-' + name.replace('_', '-') + '-fg',
                      help=name + ' foreground color')
        col_group.add('--col-' + name.replace('_', '-') + '-bg',
                      help=name + ' background color')

    args = parser.parse_args()

    # Create all necessary directories.
    for path in [args.log, args.token_path]:
        dir_maker(path)

    logging.basicConfig(filename=args.log,
                        level=logging.DEBUG if args.debug else logging.WARNING,
                        format=LOG_FORMAT)
    # urwid makes asyncio's debugging logs VERY noisy, so adjust the log level:
    logging.getLogger('asyncio').setLevel(logging.WARNING)

    datetimefmt = {'date': args.date_format,
                   'time': args.time_format}

    # setup color scheme
    palette_colors = int(args.col_palette_colors)

    col_scheme = COL_SCHEMES[args.col_scheme]
    for name in COL_SCHEME_NAMES:
        col_scheme = add_color_to_scheme(col_scheme, name,
                                         getattr(args, 'col_' + name + '_fg'),
                                         getattr(args, 'col_' + name + '_bg'),
                                         palette_colors)

    keybindings = {
        'next_tab': args.key_next_tab,
        'prev_tab': args.key_prev_tab,
        'close_tab': args.key_close_tab,
        'quit': args.key_quit,
        'menu': args.key_menu,
        'up': args.key_up,
        'down': args.key_down,
        'page_up': args.key_page_up,
        'page_down': args.key_page_down,
    }

    notifier_ = get_notifier(
        args.notification_type, args.disable_notifications
    )

    try:
        ChatUI(
            args.token_path, keybindings, col_scheme, palette_colors,
            datetimefmt, notifier_, args.discreet_notifications,
            args.manual_login
        )
    except KeyboardInterrupt:
        sys.exit('Caught KeyboardInterrupt, exiting abnormally')