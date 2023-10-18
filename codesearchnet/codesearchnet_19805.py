def headerHTML(header,fname):
        """given the bytestring ABF header, make and launch HTML."""
        html="<html><body><code>"
        html+="<h2>%s</h2>"%(fname)
        html+=pprint.pformat(header, indent=1)
        html=html.replace("\n",'<br>').replace(" ","&nbsp;")
        html=html.replace(r"\x00","")
        html+="</code></body></html>"
        print("saving header file:",fname)
        f=open(fname,'w')
        f.write(html)
        f.close()
        webbrowser.open(fname)