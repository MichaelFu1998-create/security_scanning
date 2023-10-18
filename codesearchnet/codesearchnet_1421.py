def computeAccuracy(model, size, top):
  """
  Compute prediction accuracy by checking if the next page in the sequence is
  within the top N predictions calculated by the model
  Args:
    model: HTM model
    size: Sample size
    top: top N predictions to use

  Returns: Probability the next page in the sequence is within the top N
           predicted pages
  """
  accuracy = []

  # Load MSNBC web data file
  filename = os.path.join(os.path.dirname(__file__), "msnbc990928.zip")
  with zipfile.ZipFile(filename) as archive:
    with archive.open("msnbc990928.seq") as datafile:
      # Skip header lines (first 7 lines)
      for _ in xrange(7):
        next(datafile)

      # Skip learning data and compute accuracy using only new sessions
      for _ in xrange(LEARNING_RECORDS):
        next(datafile)

      # Compute prediction accuracy by checking if the next page in the sequence
      # is within the top N predictions calculated by the model
      for _ in xrange(size):
        pages = readUserSession(datafile)
        model.resetSequenceStates()
        for i in xrange(len(pages) - 1):
          result = model.run({"page": pages[i]})
          inferences = result.inferences["multiStepPredictions"][1]

          # Get top N predictions for the next page
          predicted = sorted(inferences.items(), key=itemgetter(1), reverse=True)[:top]

          # Check if the next page is within the predicted pages
          accuracy.append(1 if pages[i + 1] in zip(*predicted)[0] else 0)

  return np.mean(accuracy)