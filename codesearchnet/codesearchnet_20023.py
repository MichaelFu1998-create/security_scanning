def html_single_basic(self,abfID,launch=False,overwrite=False):
        """
        generate a generic flat file html for an ABF parent. You could give
        this a single ABF ID, its parent ID, or a list of ABF IDs.
        If a child ABF is given, the parent will automatically be used.
        """
        if type(abfID) is str:
            abfID=[abfID]
        for thisABFid in cm.abfSort(abfID):
            parentID=cm.parent(self.groups,thisABFid)
            saveAs=os.path.abspath("%s/%s_basic.html"%(self.folder2,parentID))
            if overwrite is False and os.path.basename(saveAs) in self.files2:
                continue
            filesByType=cm.filesByType(self.groupFiles[parentID])
            html=""
            html+='<div style="background-color: #DDDDDD;">'
            html+='<span class="title">summary of data from: %s</span></br>'%parentID
            html+='<code>%s</code>'%os.path.abspath(self.folder1+"/"+parentID+".abf")
            html+='</div>'
            catOrder=["experiment","plot","tif","other"]
            categories=cm.list_order_by(filesByType.keys(),catOrder)
            for category in [x for x in categories if len(filesByType[x])]:
                if category=='experiment':
                    html+="<h3>Experimental Data:</h3>"
                elif category=='plot':
                    html+="<h3>Intrinsic Properties:</h3>"
                elif category=='tif':
                    html+="<h3>Micrographs:</h3>"
                elif category=='other':
                    html+="<h3>Additional Files:</h3>"
                else:
                    html+="<h3>????:</h3>"
                #html+="<hr>"
                #html+='<br>'*3
                for fname in filesByType[category]:
                    html+=self.htmlFor(fname)
                html+='<br>'*3
            print("creating",saveAs,'...')
            style.save(html,saveAs,launch=launch)