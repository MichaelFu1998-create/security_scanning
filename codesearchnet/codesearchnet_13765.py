def main():
    """The main entry point, compatible with setuptools."""
    # pylint: disable=bad-continuation
    from optparse import OptionParser, OptionGroup
    parser = OptionParser(usage="%prog [options] <folder path> ...",
            version="%s v%s" % (__appname__, __version__))
    parser.add_option('-D', '--defaults', action="store_true", dest="defaults",
        default=False, help="Display the default values for options which take"
        " arguments and then exit.")
    parser.add_option('-E', '--exact', action="store_true", dest="exact",
        default=False, help="There is a vanishingly small chance of false"
        " positives when comparing files using sizes and hashes. This option"
        " enables exact comparison. However, exact comparison requires a lot"
        " of disk seeks, so, on traditional moving-platter media, this trades"
        " a LOT of performance for a very tiny amount of safety most people"
        " don't need.")
    # XXX: Should I add --verbose and/or --quiet?

    filter_group = OptionGroup(parser, "Input Filtering")
    filter_group.add_option('-e', '--exclude', action="append", dest="exclude",
        metavar="PAT", help="Specify a globbing pattern to be"
        " added to the internal blacklist. This option can be used multiple"
        " times. Provide a dash (-) as your first exclude to override the"
        " pre-programmed defaults.")
    filter_group.add_option('--min-size', action="store", type="int",
        dest="min_size", metavar="X", help="Specify a non-default minimum size"
        ". Files below this size (default: %default bytes) will be ignored.")
    parser.add_option_group(filter_group)

    behaviour_group = OptionGroup(parser, "Output Behaviour")
    behaviour_group.add_option('-d', '--delete', action="store_true",
        dest="delete", help="Prompt the user for files to preserve and delete "
                            "all others.")
    behaviour_group.add_option('-n', '--dry-run', action="store_true",
        dest="dry_run", metavar="PREFIX", help="Don't actually delete any "
        "files. Just list what actions would be performed. (Good for testing "
        "values for --prefer)")
    behaviour_group.add_option('--prefer', action="append", dest="prefer",
        metavar="PATH", default=[], help="Append a globbing pattern which "
        "--delete should automatically prefer (rather than prompting) when it "
        "occurs in a list of duplicates.")
    behaviour_group.add_option('--noninteractive', action="store_true",
        dest="noninteractive", help="When using --delete, automatically assume"
        " 'all' for any groups with no --prefer matches rather than prompting")
    parser.add_option_group(behaviour_group)
    parser.set_defaults(**DEFAULTS)  # pylint: disable=W0142

    opts, args = parser.parse_args()

    if '-' in opts.exclude:
        opts.exclude = opts.exclude[opts.exclude.index('-') + 1:]
    opts.exclude = [x.rstrip(os.sep + (os.altsep or '')) for x in opts.exclude]
    # This line is required to make it match directories

    if opts.defaults:
        print_defaults()
        sys.exit()

    groups = find_dupes(args, opts.exact, opts.exclude, opts.min_size)

    if opts.delete:
        delete_dupes(groups, opts.prefer, not opts.noninteractive,
                     opts.dry_run)
    else:
        for dupeSet in groups.values():
            print '\n'.join(dupeSet) + '\n'