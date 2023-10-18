def html_index_splash(self):
        """generate landing page."""
        html="""<h1 style="background-color: #EEEEFF; padding: 10px; border: 1px solid #CCCCFF;">
        SWHLab <span style="font-size: 35%%;">%s<?span></h1>
        """%version.__version__
        #html+='<code>%s</code><br><br>'%self.abfFolder
        #html+='<hr>'
        for parent in smartSort(self.fnamesByCell.keys()):
            html+='<br><b><a href="%s.html">%s</a></b><br>'%(parent,parent)
            for child in self.fnamesByCell[parent]:
                fullpath=os.path.join(self.abfFolder,child)
                protocol = swhlab.swh_abf.abfProtocol(fullpath)
                html+='<code>%s[%s]</code><br>'%(fullpath,protocol)
        style.save(html,self.abfFolder2+"/index_splash.html")
        return