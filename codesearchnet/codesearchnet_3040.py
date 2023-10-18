def _default_stage_name_calculator(self, prefix, existing_stage_names):
    """This is the method that's implemented by the operators to get the name of the Streamlet
    :return: The name of the operator
    """
    index = 1
    calculated_name = ""
    while True:
      calculated_name = prefix + "-" + str(index)
      if calculated_name not in existing_stage_names:
        return calculated_name
      index = index + 1
    return "Should Never Got Here"