def get_hosts_retriever(s=None):
    """
    Given the function name, looks up the method for dynamically retrieving host data.
    """
    s = s or env.hosts_retriever
#     #assert s, 'No hosts retriever specified.'
    if not s:
        return env_hosts_retriever
#     module_name = '.'.join(s.split('.')[:-1])
#     func_name = s.split('.')[-1]
#     retriever = getattr(importlib.import_module(module_name), func_name)
#     return retriever
    return str_to_callable(s) or env_hosts_retriever