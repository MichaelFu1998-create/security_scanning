def POST(self, name):
    """
    /models/{name}/run

    schema:
      {
        predictedFieldName: value
        timestamp: %m/%d/%y %H:%M
      }
      NOTE: predictedFieldName MUST be the same name specified when
            creating the model.

    returns:
    {
      "predictionNumber":<number of record>,
      "anomalyScore":anomalyScore
    }
    """
    global g_models

    data = json.loads(web.data())
    data["timestamp"] = datetime.datetime.strptime(
        data["timestamp"], "%m/%d/%y %H:%M")

    if name not in g_models.keys():
      raise web.notfound("Model with name <%s> does not exist." % name)

    modelResult = g_models[name].run(data)
    predictionNumber = modelResult.predictionNumber
    anomalyScore = modelResult.inferences["anomalyScore"]

    return json.dumps({"predictionNumber": predictionNumber,
                       "anomalyScore": anomalyScore})