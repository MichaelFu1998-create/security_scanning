def delete_frames(self):
        """Delete all frames."""
        for frame in glob.glob(self.frameglob):
            os.unlink(frame)