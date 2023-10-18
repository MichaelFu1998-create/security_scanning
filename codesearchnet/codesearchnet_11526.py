def play(self, song):
        """Play callback
        """
        if song.is_ad:
            print("{} ".format(Colors.cyan("Advertisement")))
        else:
            print("{} by {}".format(Colors.cyan(song.song_name),
                                    Colors.yellow(song.artist_name)))