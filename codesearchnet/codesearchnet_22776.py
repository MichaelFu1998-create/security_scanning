def _AddPropertiesForExtensions(descriptor, cls):
  """Adds properties for all fields in this protocol message type."""
  extension_dict = descriptor.extensions_by_name
  for extension_name, extension_field in extension_dict.items():
    constant_name = extension_name.upper() + "_FIELD_NUMBER"
    setattr(cls, constant_name, extension_field.number)