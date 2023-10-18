def XMLtoPython(xmlStr=r"C:\Apps\pythonModules\GSTemp.xml"):
    """
    given a string or a path to an XML file, return an XML object.
    """
    #TODO: this absolute file path crazy stuff needs to stop!
    if os.path.exists(xmlStr):
        with open(xmlStr) as f:
            xmlStr=f.read()
    print(xmlStr)
    print("DONE")
    return