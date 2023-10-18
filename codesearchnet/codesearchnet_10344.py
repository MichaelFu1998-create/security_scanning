def scale_impropers(mol, impropers, scale, banned_lines=None):
        """Scale improper dihedrals"""
        if banned_lines is None:
                banned_lines = []
        new_impropers = []
        for im in mol.impropers:
                atypes = (im.atom1.get_atomtype(), im.atom2.get_atomtype(),
                          im.atom3.get_atomtype(), im.atom4.get_atomtype())
                atypes = [a.replace("_", "").replace("=", "") for a in atypes]

                # special-case: this is a [ dihedral ] override in molecule block, continue and don't match
                if im.gromacs['param'] != []:
                    for p in im.gromacs['param']:
                        p['kpsi'] *= scale
                    new_impropers.append(im)
                    continue

                for iswitch in range(32):
                        if  (iswitch%2==0):
                                a1=atypes[0]; a2=atypes[1]; a3=atypes[2]; a4=atypes[3];
                        else:
                                a1=atypes[3]; a2=atypes[2]; a3=atypes[1]; a4=atypes[0];
                        if((iswitch//2)%2==1): a1="X";
                        if((iswitch//4)%2==1): a2="X";
                        if((iswitch//8)%2==1): a3="X";
                        if((iswitch//16)%2==1): a4="X";
                        key = "{0}-{1}-{2}-{3}-{4}".format(a1, a2, a3, a4, im.gromacs['func'])
                        if (key in impropers):
                                for i, imt in enumerate(impropers[key]):
                                        imA = copy.deepcopy(im)
                                        param = copy.deepcopy(imt.gromacs['param'])
                                        # Only check the first dihedral in a list
                                        if not impropers[key][0].line in banned_lines:
                                                for p in param: p['kpsi'] *= scale
                                        imA.gromacs['param'] = param
                                        if i == 0:
                                                imA.comment = "; banned lines {0} found={1}\n ; parameters for types {2}-{3}-{4}-{5}-9 at LINE({6})\n".format(
                                                        " ".join(map(str, banned_lines)),
                                                        1 if imt.line in banned_lines else 0,
                                                        imt.atype1, imt.atype2, imt.atype3, imt.atype4, imt.line)
                                        new_impropers.append(imA)
                                break
        #assert(len(mol.impropers) == new_impropers)
        mol.impropers = new_impropers
        return mol