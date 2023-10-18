def _getSensorInputRecord(self, inputRecord):
    """
    inputRecord - dict containing the input to the sensor

    Return a 'SensorInput' object, which represents the 'parsed'
    representation of the input record
    """
    sensor = self._getSensorRegion()
    dataRow = copy.deepcopy(sensor.getSelf().getOutputValues('sourceOut'))
    dataDict = copy.deepcopy(inputRecord)
    inputRecordEncodings = sensor.getSelf().getOutputValues('sourceEncodings')
    inputRecordCategory = int(sensor.getOutputData('categoryOut')[0])
    resetOut = sensor.getOutputData('resetOut')[0]

    return SensorInput(dataRow=dataRow,
                       dataDict=dataDict,
                       dataEncodings=inputRecordEncodings,
                       sequenceReset=resetOut,
                       category=inputRecordCategory)