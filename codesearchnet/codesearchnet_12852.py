def _link_barcodes(self):
        """
        Private function. Links Sample barcodes in a dictionary as
        [Assembly].barcodes, with barcodes parsed from the 'barcodes_path'
        parameter. This function is called during set_params() when setting
        the barcodes_path.
        """

        ## parse barcodefile
        try:
            ## allows fuzzy match to barcodefile name
            barcodefile = glob.glob(self.paramsdict["barcodes_path"])[0]

            ## read in the file
            bdf = pd.read_csv(barcodefile, header=None, delim_whitespace=1, dtype=str)
            bdf = bdf.dropna()

            ## make sure bars are upper case
            bdf[1] = bdf[1].str.upper()

            ## if replicates are present then print a warning
            reps = bdf[0].unique().shape[0] != bdf[0].shape[0]
            if reps:
                print("{spacer}Warning: technical replicates (same name) will be combined."\
                      .format(**{'spacer': self._spacer}))
                ## add -technical-replicate-N to replicate names
                reps = [i for i in bdf[0] if list(bdf[0]).count(i) > 1]
                ureps = list(set(reps))
                for name in ureps:
                    idxs = bdf[bdf[0] == ureps[0]].index.tolist()
                    for num, idx in enumerate(idxs):
                        bdf.ix[idx][0] = bdf.ix[idx][0] + "-technical-replicate-" + str(num+1)

            ## make sure chars are all proper
            if not all(bdf[1].apply(set("RKSYWMCATG").issuperset)):
                LOGGER.warn(BAD_BARCODE)
                raise IPyradError(BAD_BARCODE)

            ## 3rad/seqcap use multiplexed barcodes
            ## We'll concatenate them with a plus and split them later
            if "3rad" in self.paramsdict["datatype"]:
                try:
                    bdf[2] = bdf[2].str.upper()
                    self.barcodes = dict(zip(bdf[0], bdf[1] + "+" + bdf[2]))
                except KeyError as inst:
                    msg = "    3rad assumes multiplexed barcodes. Doublecheck your barcodes file."
                    LOGGER.error(msg)
                    raise IPyradError(msg)
            else:
                ## set attribute on Assembly object
                self.barcodes = dict(zip(bdf[0], bdf[1]))

        except (IOError, IndexError):
            raise IPyradWarningExit(\
                "    Barcodes file not found. You entered: {}"\
                .format(self.paramsdict["barcodes_path"]))

        except ValueError as inst:
            msg = "    Barcodes file format error."
            LOGGER.warn(msg)
            raise IPyradError(inst)