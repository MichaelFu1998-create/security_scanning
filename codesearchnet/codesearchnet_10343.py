def scale_dihedrals(mol, dihedrals, scale, banned_lines=None):
        """Scale dihedral angles"""

        if banned_lines is None:
                banned_lines = []
        new_dihedrals = []
        for dh in mol.dihedrals:
                atypes = dh.atom1.get_atomtype(), dh.atom2.get_atomtype(), dh.atom3.get_atomtype(), dh.atom4.get_atomtype()
                atypes = [a.replace("_", "").replace("=","") for a in atypes]

                # special-case: this is a [ dihedral ] override in molecule block, continue and don't match
                if dh.gromacs['param'] != []:
                    for p in dh.gromacs['param']:
                        p['kch'] *= scale
                    new_dihedrals.append(dh)
                    continue

                for iswitch in range(32):
                        if  (iswitch%2==0 ):
                                a1=atypes[0]; a2=atypes[1]; a3=atypes[2]; a4=atypes[3]
                        else:
                                a1=atypes[3]; a2=atypes[2]; a3=atypes[1]; a4=atypes[0]

                        if((iswitch//2)%2==1): a1="X";
                        if((iswitch//4)%2==1): a2="X";
                        if((iswitch//8)%2==1): a3="X";
                        if((iswitch//16)%2==1): a4="X";
                        key = "{0}-{1}-{2}-{3}-{4}".format(a1, a2, a3, a4, dh.gromacs['func'])
                        if (key in dihedrals):
                                for i, dt in enumerate(dihedrals[key]):
                                        dhA = copy.deepcopy(dh)
                                        param = copy.deepcopy(dt.gromacs['param'])
                                        # Only check the first dihedral in a list
                                        if not dihedrals[key][0].line in banned_lines:
                                                for p in param: p['kchi'] *= scale
                                        dhA.gromacs['param'] = param
                                        #if key == "CT3-C-NH1-CT1-9": print i, dt, key
                                        if i == 0:
                                                dhA.comment = "; banned lines {0} found={1}\n".format(" ".join(
                                                        map(str, banned_lines)), 1 if dt.line in banned_lines else 0)
                                                dhA.comment += "; parameters for types {}-{}-{}-{}-9 at LINE({})\n".format(
                                                        dhA.atom1.atomtype, dhA.atom2.atomtype, dhA.atom3.atomtype,
                                                        dhA.atom4.atomtype, dt.line).replace("_","")
                                        name = "{}-{}-{}-{}-9".format(dhA.atom1.atomtype, dhA.atom2.atomtype,
                                                                      dhA.atom3.atomtype, dhA.atom4.atomtype).replace("_","")
                                        #if name == "CL-CTL2-CTL2-HAL2-9": print dihedrals[key], key
                                        new_dihedrals.append(dhA)
                                break


        mol.dihedrals = new_dihedrals
        #assert(len(mol.dihedrals) == new_dihedrals)
        return mol