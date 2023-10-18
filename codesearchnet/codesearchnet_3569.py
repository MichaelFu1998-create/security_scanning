def concretized_args(**policies):
    """
    Make sure an EVM instruction has all of its arguments concretized according to
    provided policies.

    Example decoration:

        @concretized_args(size='ONE', address='')
        def LOG(self, address, size, *topics):
            ...

    The above will make sure that the |size| parameter to LOG is Concretized when symbolic
    according to the 'ONE' policy and concretize |address| with the default policy.

    :param policies: A kwargs list of argument names and their respective policies.
                         Provide None or '' as policy to use default.
    :return: A function decorator
    """
    def concretizer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            spec = inspect.getfullargspec(func)
            for arg, policy in policies.items():
                assert arg in spec.args, "Concretizer argument not found in wrapped function."
                # index is 0-indexed, but ConcretizeArgument is 1-indexed. However, this is correct
                # since implementation method is always a bound method (self is param 0)
                index = spec.args.index(arg)
                if not issymbolic(args[index]):
                    continue
                if not policy:
                    policy = 'SAMPLED'

                if policy == "ACCOUNTS":
                    value = args[index]
                    world = args[0].world
                    #special handler for EVM only policy
                    cond = world._constraint_to_accounts(value, ty='both', include_zero=True)
                    world.constraints.add(cond)
                    policy = 'ALL'
                raise ConcretizeArgument(index, policy=policy)
            return func(*args, **kwargs)
        wrapper.__signature__ = inspect.signature(func)
        return wrapper
    return concretizer