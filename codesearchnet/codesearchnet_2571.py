def load(file_object):
  """
  Deserializes Java primitive data and objects serialized by ObjectOutputStream
  from a file-like object.
  """
  marshaller = JavaObjectUnmarshaller(file_object)
  marshaller.add_transformer(DefaultObjectTransformer())
  return marshaller.readObject()