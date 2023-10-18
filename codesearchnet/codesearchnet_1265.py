def _abbreviate(text, threshold):
  """ Abbreviate the given text to threshold chars and append an ellipsis if its
  length exceeds threshold; used for logging;

  NOTE: the resulting text could be longer than threshold due to the ellipsis
  """
  if text is not None and len(text) > threshold:
    text = text[:threshold] + "..."

  return text