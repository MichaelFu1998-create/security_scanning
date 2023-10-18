def run_global_hook(hook_name, *args):
    '''Attempt to run a global hook by name with args'''

    hook_finder = HookFinder(get_global_hook_path())
    hook = hook_finder(hook_name)
    if hook:
        hook.run(*args)