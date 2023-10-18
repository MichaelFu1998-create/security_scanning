def htmlFor(self,fname):
        """return appropriate HTML determined by file extension."""
        if os.path.splitext(fname)[1].lower() in ['.jpg','.png']:
            html='<a href="%s"><img src="%s"></a>'%(fname,fname)
            if "_tif_" in fname:
                html=html.replace('<img ','<img class="datapic micrograph"')
            if "_plot_" in fname:
                html=html.replace('<img ','<img class="datapic intrinsic" ')
            if "_experiment_" in fname:
                html=html.replace('<img ','<img class="datapic experiment" ')
        elif os.path.splitext(fname)[1].lower() in ['.html','.htm']:
            html='LINK: %s'%fname
        else:
            html='<br>Not sure how to show: [%s]</br>'%fname
        return html