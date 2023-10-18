def monitor(self, sleep=5):
        """Run file modification monitor.

        The monitor can catch file modification using timestamp and file body. 
        Monitor has timestamp data and file body data. And insert timestamp 
        data and file body data before into while roop. In while roop, monitor 
        get new timestamp and file body, and then monitor compare new timestamp
        to originaltimestamp. If new timestamp and file body differ original,
        monitor regard thease changes as `modification`. Then monitor create
        instance of FileModificationObjectManager and FileModificationObject,
        and monitor insert FileModificationObject to FileModificationObject-
        Manager. Then, yield this object.

        :param sleep: How times do you sleep in while roop.
        """


        manager = FileModificationObjectManager()

        timestamps = {}
        filebodies = {}

        # register original timestamp and filebody to dict
        for file in self.f_repository:
            timestamps[file] = self._get_mtime(file)
            filebodies[file] = open(file).read()


        while True:

            for file in self.f_repository:

                mtime = timestamps[file]
                fbody = filebodies[file]

                modified = self._check_modify(file, mtime, fbody)

                # file not modify -> continue
                if not modified:
                    continue

                # file modifies -> create the modification object

                new_mtime = self._get_mtime(file)
                new_fbody = open(file).read()

                obj = FileModificationObject(
                        file,
                        (mtime, new_mtime),
                        (fbody, new_fbody) )

                # overwrite new timestamp and filebody
                timestamps[file] = new_mtime
                filebodies[file] = new_fbody


                # append file modification object to manager
                manager.add_object(obj)

                # return new modification object
                yield obj

            time.sleep(sleep)