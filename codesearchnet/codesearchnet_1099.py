def getExperimentDescriptionInterfaceFromModule(module):
  """
  :param module: imported description.py module

  :returns: (:class:`nupic.frameworks.opf.exp_description_api.DescriptionIface`)
            represents the experiment description
  """
  result = module.descriptionInterface
  assert isinstance(result, exp_description_api.DescriptionIface), \
         "expected DescriptionIface-based instance, but got %s" % type(result)

  return result