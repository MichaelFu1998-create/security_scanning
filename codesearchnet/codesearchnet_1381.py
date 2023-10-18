def POST(self, name):
    """
    /models/{name}

    schema:
    {
      "modelParams": dict containing model parameters
      "predictedFieldName": str
    }

    returns:
    {"success":name}
    """
    global g_models

    data = json.loads(web.data())
    modelParams = data["modelParams"]
    predictedFieldName = data["predictedFieldName"]

    if name in g_models.keys():
      raise web.badrequest("Model with name <%s> already exists" % name)

    model = ModelFactory.create(modelParams)
    model.enableInference({'predictedField': predictedFieldName})
    g_models[name] = model

    return json.dumps({"success": name})