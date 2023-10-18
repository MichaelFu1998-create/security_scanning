def loads(string):
  """
  Deserializes Java objects and primitive data serialized by ObjectOutputStream
  from a string.
  """
  f = StringIO.StringIO(string)
  marshaller = JavaObjectUnmarshaller(f)
  marshaller.add_transformer(DefaultObjectTransformer())
  return marshaller.readObject()