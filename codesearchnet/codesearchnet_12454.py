def _train_and_save(obj, cache, data, print_updates):
    """Internal pickleable function used to train objects in another process"""
    obj.train(data)
    if print_updates:
        print('Regenerated ' + obj.name + '.')
    obj.save(cache)