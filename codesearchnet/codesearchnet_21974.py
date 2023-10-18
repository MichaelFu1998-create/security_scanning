def prepareImages(self, fileName, logType):
        """Convert supplied QPixmap object to image file."""
        import subprocess
        
        if self.imageType == "png":
            self.imagePixmap.save(fileName + ".png", "PNG", -1)
            if logType == "Physics":
                makePostScript = "convert " + fileName + ".png " + fileName + ".ps"
                process = subprocess.Popen(makePostScript, shell=True)
                process.wait()
                thumbnailPixmap = self.imagePixmap.scaled(500, 450, Qt.KeepAspectRatio)
                thumbnailPixmap.save(fileName + ".png", "PNG", -1)
        else:
            renameImage = "cp " + self.image + " " + fileName + ".gif"
            process = subprocess.Popen(renameImage, shell=True)
            process.wait()
            if logType == "Physics":
                thumbnailPixmap = self.imagePixmap.scaled(500, 450, Qt.KeepAspectRatio)
                thumbnailPixmap.save(fileName + ".png", "PNG", -1)