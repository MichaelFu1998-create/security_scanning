def root_path():
    """Get the absolute path to the root of the demosys package"""
    module_dir = os.path.dirname(globals()['__file__'])
    return os.path.dirname(os.path.dirname(module_dir))