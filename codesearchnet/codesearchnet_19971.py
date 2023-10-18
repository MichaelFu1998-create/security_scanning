def headerHTML(self,fname=None):
        """read the ABF header and save it HTML formatted."""
        if fname is None:
            fname = self.fname.replace(".abf","_header.html")
        html="<html><body><code>"
        html+="<h2>abfinfo() for %s.abf</h2>"%self.ID
        html+=self.abfinfo().replace("<","&lt;").replace(">","&gt;").replace("\n","<br>")
        html+="<h2>Header for %s.abf</h2>"%self.ID
        html+=pprint.pformat(self.header, indent=1)
        html=html.replace("\n",'<br>').replace(" ","&nbsp;")
        html=html.replace(r"\x00","")
        html+="</code></body></html>"
        print("WRITING HEADER TO:")
        print(fname)
        f=open(fname,'w')
        f.write(html)
        f.close()