def save(self):
        """ Save repository .pyrepinfo to disk. """
        # open file
        repoInfoPath = os.path.join(self.__path, ".pyrepinfo")
        try:
            fdinfo = open(repoInfoPath, 'wb')
        except Exception as e:
            raise Exception("unable to open repository info for saving (%s)"%e)
        # save repository
        try:
            pickle.dump( self, fdinfo, protocol=2 )
        except Exception as e:
            fdinfo.flush()
            os.fsync(fdinfo.fileno())
            fdinfo.close()
            raise Exception( "Unable to save repository info (%s)"%e )
        finally:
            fdinfo.flush()
            os.fsync(fdinfo.fileno())
            fdinfo.close()
        # save timestamp
        repoTimePath = os.path.join(self.__path, ".pyrepstate")
        try:
            self.__state = ("%.6f"%time.time()).encode()
            with open(repoTimePath, 'wb') as fdtime:
                fdtime.write( self.__state )
                fdtime.flush()
                os.fsync(fdtime.fileno())
        except Exception as e:
            raise Exception("unable to open repository time stamp for saving (%s)"%e)