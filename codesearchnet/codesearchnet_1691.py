def learn(self, bottomUpInput, enableInference=None):
    """
    TODO: document

    :param bottomUpInput: 
    :param enableInference: 
    :return: 
    """
    return self.compute(bottomUpInput, enableLearn=True,
                        enableInference=enableInference)