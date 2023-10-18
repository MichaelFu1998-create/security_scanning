def partial_tempering(topfile="processed.top", outfile="scaled.top", banned_lines='',
                      scale_lipids=1.0, scale_protein=1.0):
        """Set up topology for partial tempering (REST2) replica exchange.


        .. versionchanged:: 0.7.0
           Use keyword arguments instead of an `args` Namespace object.
        """

        banned_lines = map(int, banned_lines.split())
        top = TOP(topfile)
        groups = [("_", float(scale_protein)), ("=", float(scale_lipids))]

        #
        # CMAPTYPES
        #
        cmaptypes = []
        for ct in top.cmaptypes:
                cmaptypes.append(ct)
                for gr, scale in groups:
                        ctA = copy.deepcopy(ct)
                        ctA.atype1 += gr
                        ctA.atype2 += gr
                        ctA.atype3 += gr
                        ctA.atype4 += gr
                        ctA.atype8 += gr
                        ctA.gromacs['param'] = [ v*scale for v in ct.gromacs['param'] ]
                        cmaptypes.append(ctA)
        logger.debug("cmaptypes was {0}, is {1}".format(len(top.cmaptypes), len(cmaptypes)))
        top.cmaptypes = cmaptypes


        #
        # ATOMTYPES
        #
        atomtypes = []
        for at in top.atomtypes:
                atomtypes.append(at)
                for gr, scale in groups:
                        atA = copy.deepcopy(at)
                        atA.atnum = atA.atype
                        atA.atype += gr
                        atA.gromacs['param']['lje'] *= scale
                        atomtypes.append(atA)
        top.atomtypes = atomtypes

        #
        # PAIRTYPES
        #
        pairtypes = []
        for pt in top.pairtypes:
                pairtypes.append(pt)
                for gr, scale in groups:
                        ptA = copy.deepcopy(pt)
                        ptA.atype1 += gr
                        ptA.atype2 += gr
                        ptA.gromacs['param']['lje14'] *= scale

                        pairtypes.append(ptA)
        top.pairtypes = pairtypes

        #
        # BONDTYPES
        #
        bondtypes = []
        for bt in top.bondtypes:
                bondtypes.append(bt)
                for gr, scale in groups:
                        btA = copy.deepcopy(bt)
                        btA.atype1 += gr
                        btA.atype2 += gr
                        bondtypes.append(btA)
        top.bondtypes = bondtypes


        #
        # ANGLETYPES
        #
        angletypes = []
        for at in top.angletypes:
                angletypes.append(at)
                for gr, scale in groups:
                        atA = copy.deepcopy(at)
                        atA.atype1 += gr
                        atA.atype2 += gr
                        atA.atype3 += gr
                        angletypes.append(atA)
        top.angletypes = angletypes

        #
        # Build dihedral dictionary
        #
        dihedraltypes = {}
        for dt in top.dihedraltypes:
                dt.disabled = True
                dt.comment = "; type={0!s}-{1!s}-{2!s}-{3!s}-9\n; LINE({4:d}) ".format(
                        dt.atype1, dt.atype2, dt.atype3, dt.atype4, dt.line)
                dt.comment = dt.comment.replace("_","")

                #if "X-CTL2-CTL2-X-9" in dt.comment: print dt
                name = "{0}-{1}-{2}-{3}-{4}".format(dt.atype1, dt.atype2, dt.atype3, dt.atype4, dt.gromacs['func'])
                if not name in dihedraltypes:
                        dihedraltypes[name] = []
                dihedraltypes[name].append(dt)
        logger.debug("Build dihedraltypes dictionary with {0} entries".format(len(dihedraltypes)))

        #
        # Build improper dictionary
        #
        impropertypes = {}
        for it in top.impropertypes:
                it.disabled = True
                it.comment = "; LINE({0:d}) ".format(it.line)
                name = "{0}-{1}-{2}-{3}-{4}".format(
                        it.atype1, it.atype2, it.atype3, it.atype4, it.gromacs['func'])
                if not name in impropertypes:
                        impropertypes[name] = []
                impropertypes[name].append(it)
        logger.debug("Build impropertypes dictionary with {0} entries".format(len(impropertypes)))

        for molname_mol in top.dict_molname_mol:
            if not 'Protein' in molname_mol:
                continue
            mol = top.dict_molname_mol[molname_mol]
            for at in mol.atoms:
                at.charge *= math.sqrt(scale_protein)
            mol = scale_dihedrals(mol, dihedraltypes, scale_protein, banned_lines)
            mol = scale_impropers(mol, impropertypes, 1.0, banned_lines)

        top.write(outfile)