def analyze(self, output_folder=".", auto_remove=False):
        """
        :type auto_remove: boolean
        :param boolean auto_remove: auto remove previous files in analyze folder
        """
        if auto_remove:
            try:
                shutil.rmtree(output_folder)
            except:
                pass
        try:
            mkdir(output_folder)
        except:
            pass
        tokens = [token for sublist in self.sentences for token in sublist]
        df = pd.DataFrame(tokens)
        log = u""
        log += u"Sentences    : {}\n".format(len(self.sentences))
        n = df.shape[1]
        log += self._analyze_first_token(df, 0, output_folder)
        for i in range(1, n):
            log += self._analyze_field(df, i, output_folder)
        print(log)
        stat_file = join(output_folder, "stats.txt")
        write(stat_file, log)