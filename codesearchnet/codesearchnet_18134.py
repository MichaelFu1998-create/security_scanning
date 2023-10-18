def _check_for_inception(self, root_dict):
    '''
      Used to check if there is a dict in a dict
    '''

    for key in root_dict:
      if isinstance(root_dict[key], dict):
          root_dict[key] = ResponseObject(root_dict[key])

    return root_dict