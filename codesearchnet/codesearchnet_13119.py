def parse(self, psearch, dsearch):
        """ parse an _f structure output file """
        stable = ""
        with open(self.repfile) as orep:
            dat = orep.readlines()
            for line in dat:
                ## stat lines
                if "Estimated Ln Prob of Data" in line:
                    self.est_lnlik = float(line.split()[-1])
                if "Mean value of ln likelihood" in line:
                    self.mean_lnlik = float(line.split()[-1])
                if "Variance of ln likelihood" in line:
                    self.var_lnlik = float(line.split()[-1])
                if "Mean value of alpha" in line:
                    self.alpha = float(line.split()[-1])

                ## matrix lines
                nonline = psearch.search(line)
                popline = dsearch.search(line)

                #if ")   :  " in line:
                if nonline:
                    ## check if sample is supervised...
                    abc = line.strip().split()
                    outstr = "{}{}{}".format(
                        " ".join([abc[0], abc[0], abc[2], 
                                  abc[0].split('.')[0]]),
                        " :  ",
                        " ".join(abc[4:])
                    )
                    self.inds += 1
                    stable += outstr+"\n"

                elif popline:
                    ## check if sample is supervised...
                    abc = line.strip().split()
                    prop = ["0.000"] * self.kpop
                    pidx = int(abc[3]) - 1
                    prop[pidx] = "1.000"
                    outstr = "{}{}{}".format(
                        " ".join([abc[0], abc[0], abc[2], 
                                  abc[0].split('.')[0]]),
                        " :  ",
                        " ".join(prop)
                    )
                    self.inds += 1
                    stable += outstr+"\n"

            stable += "\n"
        return stable