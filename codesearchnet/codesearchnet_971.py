def _generateFileFromTemplates(templateFileNames, outputFilePath,
                              replacementDict):
  """ Generates a file by applying token replacements to the given template
  file

  templateFileName:
                  A list of template file names; these files are assumed to be in
                  the same directory as the running experiment_generator.py script.
                  ExpGenerator will perform the substitution and concanetate
                  the files in the order they are specified

  outputFilePath: Absolute path of the output file

  replacementDict:
                  A dictionary of token/replacement pairs
  """

  # Find out where we're running from so we know where to find templates
  installPath = os.path.dirname(__file__)
  outputFile = open(outputFilePath, "w")
  outputLines = []
  inputLines = []

  firstFile = True
  for templateFileName in templateFileNames:
    # Separate lines from each file by two blank lines.
    if not firstFile:
      inputLines.extend([os.linesep]*2)
    firstFile = False

    inputFilePath = os.path.join(installPath, templateFileName)
    inputFile = open(inputFilePath)
    inputLines.extend(inputFile.readlines())
    inputFile.close()


  print "Writing ", len(inputLines), "lines..."

  for line in inputLines:
    tempLine = line

    # Enumerate through each key in replacementDict and replace with value
    for k, v in replacementDict.iteritems():
      if v is None:
        v = "None"
      tempLine = re.sub(k, v, tempLine)
    outputFile.write(tempLine)
  outputFile.close()