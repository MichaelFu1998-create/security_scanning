def run_hook(hook, config, quiet=False):
    """Run post-bootstrap hook if any.

    :param hook: Hook to run.
    :param config: Configuration dict.
    :param quiet: Do not output messages to STDOUT/STDERR. By default: False
    """
    if not hook:
        return True

    if not quiet:
        print_message('== Step 3. Run post-bootstrap hook ==')

    result = not run_cmd(prepare_args(hook, config),
                         echo=not quiet,
                         fail_silently=True,
                         shell=True)

    if not quiet:
        print_message()

    return result