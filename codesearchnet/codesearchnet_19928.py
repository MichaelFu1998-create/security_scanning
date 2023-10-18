def makePics(self):
        """convert every .image we find to a ./swhlab/ image"""
        rescanNeeded=False
        for fname in smartSort(self.fnames):
            if fname in self.fnames2:
                continue
            ext=os.path.splitext(fname)[1].lower()
            if ext in [".jpg",".png"]:
                if not fname in self.abfFolder2:
                    self.log.debug("copying %s",fname)
                    shutil.copy(os.path.join(self.abfFolder,fname),os.path.join(self.abfFolder2,fname))
                    rescanNeeded=True
            if ext in [".tif",".tiff"]:
                if not fname+".jpg" in self.fnames2:
                    self.log.debug("converting %s",fname)
                    swhlab.swh_image.TIF_to_jpg(os.path.join(self.abfFolder,fname),saveAs=os.path.join(self.abfFolder2,fname+".jpg"))
                    rescanNeeded=True
        if rescanNeeded:
            self.log.debug("new pics, so a rescan is needed...")
            self.log.debug("REBUILDING ALL RECOMMENDED!!!!!!!!!!!")
            self.folderScan()