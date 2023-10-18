def format(self):
        """
        Dictionary of available formats, corresponding to a list of the values
        Example: pod.format['plaintext'] will return a list of every plaintext
                 content in the pod's subpods
        """
        formats = {}

        # Iterate through all the tags (formats) in subpods
        # 'state' is a tag but not an acceptable format
        for subpod in self.root.findall('subpod'):

            # elem will be a specific format
            for elem in list(subpod):

                # skip any subpod state xml groups (not a format)
                if elem.tag == 'state':
                    continue

                # Content of elem (specific format)
                content = elem.text

                # img needs special content packaging
                if elem.tag == 'img':
                    content = {'url': elem.get('src'),
                               'alt': elem.get('alt'),
                               'title': elem.get('title'),
                               'width': int(elem.get('width', 0)),
                               'height': int(elem.get('height', 0))}

                # Create / append to return dict
                if elem.tag not in formats:
                    formats[elem.tag] = [content]
                else:
                    formats[elem.tag].append(content)

        return formats