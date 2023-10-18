def processArgs():
    """check out the arguments and figure out what to do."""
    if len(sys.argv)<2:
        print("\n\nERROR:")
        print("this script requires arguments!")
        print('try "python command.py info"')
        return
    if sys.argv[1]=='info':
        print("import paths:\n ","\n  ".join(sys.path))
        print()
        print("python version:",sys.version)
        print("SWHLab path:",__file__)
        print("SWHLab version:",swhlab.__version__)
        return
    if sys.argv[1]=='glanceFolder':
        abfFolder=swhlab.common.gui_getFolder()
        if not abfFolder or not os.path.isdir(abfFolder):
            print("bad path")
            return
        fnames=sorted(glob.glob(abfFolder+"/*.abf"))
        outFolder=tempfile.gettempdir()+"/swhlab/"
        if os.path.exists(outFolder):
            shutil.rmtree(outFolder)
        os.mkdir(outFolder)
        outFile=outFolder+"/index.html"
        out='<html><body>'
        out+='<h2>%s</h2>'%abfFolder
        for i,fname in enumerate(fnames):
            print("\n\n### PROCESSING %d of %d"%(i,len(fnames)))
            saveAs=os.path.join(os.path.dirname(outFolder),os.path.basename(fname))+".png"
            out+='<br><br><br><code>%s</code><br>'%os.path.abspath(fname)
            out+='<a href="%s"><img src="%s"></a><br>'%(saveAs,saveAs)
            swhlab.analysis.glance.processAbf(fname,saveAs)
        out+='</body></html>'
        with open(outFile,'w') as f:
            f.write(out)
        webbrowser.open_new_tab(outFile)
        return


    print("\n\nERROR:\nI'm not sure how to process these arguments!")
    print(sys.argv)