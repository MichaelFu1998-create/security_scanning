def get_exif_info(self):
        """return exif-tag dict
        """
        _dict = {}
        for tag in _EXIF_TAGS:
            ret = self.img.attribute("EXIF:%s" % tag)
            if ret and ret != 'unknown':
                _dict[tag] = ret
        return _dict