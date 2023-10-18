def convertImages(self):
        """
        run this to turn all folder1 TIFs and JPGs into folder2 data.
        TIFs will be treated as micrographs and converted to JPG with enhanced
        contrast. JPGs will simply be copied over.
        """

        # copy over JPGs (and such)
        exts=['.jpg','.png']
        for fname in [x for x in self.files1 if cm.ext(x) in exts]:
            ID="UNKNOWN"
            if len(fname)>8 and fname[:8] in self.IDs:
                ID=fname[:8]
            fname2=ID+"_jpg_"+fname
            if not fname2 in self.files2:
                self.log.info("copying over [%s]"%fname2)
                shutil.copy(os.path.join(self.folder1,fname),os.path.join(self.folder2,fname2))
            if not fname[:8]+".abf" in self.files1:
                self.log.error("orphan image: %s",fname)

        # convert TIFs (and such) to JPGs
        exts=['.tif','.tiff']
        for fname in [x for x in self.files1 if cm.ext(x) in exts]:
            ID="UNKNOWN"
            if len(fname)>8 and fname[:8] in self.IDs:
                ID=fname[:8]
            fname2=ID+"_tif_"+fname+".jpg"
            if not fname2 in self.files2:
                self.log.info("converting micrograph [%s]"%fname2)
                imaging.TIF_to_jpg(os.path.join(self.folder1,fname),saveAs=os.path.join(self.folder2,fname2))
            if not fname[:8]+".abf" in self.files1:
                self.log.error("orphan image: %s",fname)