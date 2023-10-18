def _parse(self, fname):
        """Parse a processed.top GROMACS topology file

        The function reads in the file line-by-line, and it's a bunch of 'elif' statements,
        writing parameter/atom line to current section/molecule.

        ParamTypes are added to self.xyztypes (AtomType goes to self.atomtypes).
        Params are added to current molecule (Atom goes to mol.atoms.append(atom))

        MoleculeTypes and Molecules are odd, and are added to
            * MoleculeType to :attr:`self.dict_molname_mol[mol.name] = mol`
            * Molecule to :attr:`self.molecules.append(self.dict_molname_mol[mname])`

        :obj:`curr_sec` variable stores to current section being read-in
        :obj:`mol` variable stores the current molecule being read-in
        :obj:`cmap_lines` are a little odd, since CMAP parameters are stored on multiple lines

        :Arguments:
          *fname*
              name of the processed.top file

        :Returns: None
        """
        def _find_section(line):
            return  line.strip('[').strip(']').strip()

        def _add_info(sys_or_mol, section, container):
            # like (mol, 'atomtypes', mol.atomtypes)
            if sys_or_mol.information.get(section, False) is False:
                sys_or_mol.information[section] = container

        mol        = None   # to hold the current mol
        curr_sec   = None
        cmap_lines = []

        with open(fname) as f:
            for i_line, line in enumerate(f):

                # trimming
                if ';' in line:
                    line = line[0:line.index(';')]
                line = line.strip()

                if line == '':
                    continue

                if line[0] == '*':
                    continue

                # the topology must be stand-alone (i.e. no includes)
                if line.startswith('#include'):
                    msg = 'The topology file has "#include" statements.'
                    msg+= ' You must provide a processed topology file that grompp creates.'
                    raise ValueError(msg)

                # find sections
                if line[0] == '[':
                    curr_sec = _find_section(line)
                    self.found_sections.append(curr_sec)
                    continue

                fields = line.split()

                if curr_sec == 'defaults':
                    '''
                    # ; nbfunc        comb-rule       gen-pairs       fudgeLJ fudgeQQ
                    #1               2               yes             0.5     0.8333
                    '''
                    assert len(fields) in  [2, 5]
                    self.defaults['nbfunc']    = int(fields[0])
                    self.defaults['comb-rule'] = int(fields[1])
                    if len(fields) == 5:

                       self.defaults['gen-pairs'] = fields[2]
                       self.defaults['fudgeLJ']   = float(fields[3])
                       self.defaults['fudgeQQ']   = float(fields[4])

                elif curr_sec == 'atomtypes':
                    '''
                    # ;name               at.num    mass         charge    ptype  sigma   epsilon
                    # ;name   bond_type   at.num    mass         charge    ptype  sigma   epsilon
                    # ;name                         mass         charge    ptype  c6      c12

                    '''
                    if len(fields) not in (6,7,8):
                        self.logger.warning('skipping atomtype line with neither 7 or 8 fields: \n {0:s}'.format(line))
                        continue

                    #shift = 0 if len(fields) == 7 else 1
                    shift = len(fields) - 7
                    at = blocks.AtomType('gromacs')
                    at.atype = fields[0]
                    if shift == 1: at.bond_type = fields[1]

                    at.mass  = float(fields[2+shift])
                    at.charge= float(fields[3+shift])

                    particletype = fields[4+shift]
                    assert particletype in ('A', 'S', 'V', 'D')
                    if particletype not in ('A',):
                        self.logger.warning('warning: non-atom particletype: "{0:s}"'.format(line))

                    sig = float(fields[5+shift])
                    eps = float(fields[6+shift])

                    at.gromacs= {'param': {'lje':eps, 'ljl':sig, 'lje14':None, 'ljl14':None} }

                    self.atomtypes.append(at)

                    _add_info(self, curr_sec, self.atomtypes)


                # extend system.molecules
                elif curr_sec == 'moleculetype':
                    assert len(fields) == 2

                    mol = blocks.Molecule()

                    mol.name = fields[0]
                    mol.exclusion_numb = int(fields[1])

                    self.dict_molname_mol[mol.name] = mol


                elif curr_sec == 'atoms':
                    '''
                    #id    at_type     res_nr  residu_name at_name  cg_nr  charge   mass  typeB    chargeB      massB
                    # 1       OC          1       OH          O1       1      -1.32

                    OR

                    [ atoms ]
                    ; id   at type  res nr  residu name at name     cg nr   charge
                    1       OT      1       SOL              OW             1       -0.834

                    '''

                    aserial = int(fields[0])
                    atype   = fields[1]
                    resnumb = int(fields[2])
                    resname = fields[3]
                    aname   = fields[4]
                    cgnr    = int(fields[5])
                    charge  = float(fields[6])
                    rest = fields[7:]

                    atom         = blocks.Atom()
                    atom.name    = aname
                    atom.atomtype= atype
                    atom.number  = aserial
                    atom.resname = resname
                    atom.resnumb = resnumb
                    atom.charge  = charge

                    if rest:
                        mass = float(rest[0])
                        atom.mass = mass

                    mol.atoms.append(atom)

                    _add_info(mol, curr_sec, mol.atoms)

                elif curr_sec in ('pairtypes', 'pairs', 'pairs_nb'):
                    '''
                    section     #at     fu      #param
                    ---------------------------------
                    pairs       2       1       V,W
                    pairs       2       2       fudgeQQ, qi, qj, V, W
                    pairs_nb    2       1       qi, qj, V, W

                    '''

                    ai, aj = fields[:2]
                    fu     = int(fields[2])
                    assert fu in (1,2)

                    pair = blocks.InteractionType('gromacs')
                    if fu == 1:
                        if curr_sec=='pairtypes':
                            pair.atype1 = ai
                            pair.atype2 = aj
                            v, w = list(map(float, fields[3:5]))
                            pair.gromacs = {'param': {'lje':None, 'ljl':None, 'lje14':w, 'ljl14':v}, 'func':fu }

                            self.pairtypes.append(pair)
                            _add_info(self, curr_sec, self.pairtypes)

                        elif curr_sec == 'pairs':
                            ai, aj = list( map(int, [ai,aj]) )
                            pair.atom1 = mol.atoms[ai-1]
                            pair.atom2 = mol.atoms[aj-1]
                            pair.gromacs['func'] = fu

                            mol.pairs.append(pair)
                            _add_info(mol, curr_sec, mol.pairs)

                        else:
                            raise ValueError

                    else:
                        raise NotImplementedError('{0:s} with functiontype {1:d} is not supported'.format(curr_sec,fu))

                elif curr_sec == 'nonbond_params':
                    '''
                    ; typei typej  f.type sigma   epsilon
                    ; f.type=1 means LJ (not buckingham)
                    ; sigma&eps since mixing-rule = 2
                    '''

                    assert len(fields) == 5
                    ai, aj = fields[:2]
                    fu     = int(fields[2])

                    assert fu == 1
                    sig    = float(fields[3])
                    eps    = float(fields[4])

                    nonbond_param = blocks.NonbondedParamType('gromacs')
                    nonbond_param.atype1 = ai
                    nonbond_param.atype2 = aj
                    nonbond_param.gromacs['func'] = fu
                    nonbond_param.gromacs['param'] = {'eps': eps, 'sig': sig}

                    self.nonbond_params.append(nonbond_param)
                    _add_info(self, curr_sec, self.nonbond_params)

                elif curr_sec in ('bondtypes', 'bonds'):
                    '''
                    section     #at     fu      #param
                    ----------------------------------
                    bonds       2       1       2
                    bonds       2       2       2
                    bonds       2       3       3
                    bonds       2       4       2
                    bonds       2       5       ??
                    bonds       2       6       2
                    bonds       2       7       2
                    bonds       2       8       ??
                    bonds       2       9       ??
                    bonds       2       10      4
                    '''

                    ai, aj = fields[:2]
                    fu     = int(fields[2])
                    assert fu in (1,2,3,4,5,6,7,8,9,10)

                    if fu != 1:
                        raise NotImplementedError('function {0:d} is not yet supported'.format(fu))

                    bond = blocks.BondType('gromacs')

                    if fu == 1:
                        if curr_sec == 'bondtypes':
                            bond.atype1 = ai
                            bond.atype2 = aj

                            b0, kb = list(map(float, fields[3:5]))
                            bond.gromacs = {'param':{'kb':kb, 'b0':b0}, 'func':fu}

                            self.bondtypes.append(bond)
                            _add_info(self, curr_sec, self.bondtypes)

                        elif curr_sec == 'bonds':
                            ai, aj = list(map(int, [ai, aj]))
                            bond.atom1 = mol.atoms[ai-1]
                            bond.atom2 = mol.atoms[aj-1]
                            bond.gromacs['func'] = fu

                            if len(fields) > 3:
                                b0, kb = list(map(float, fields[3:5]))
                                bond.gromacs = {'param':{'kb':kb, 'b0':b0}, 'func':fu}

                            mol.bonds.append(bond)
                            _add_info(mol, curr_sec, mol.bonds)

                    else:
                        raise NotImplementedError

                elif curr_sec in ('angletypes', 'angles'):
                    '''
                    section     #at     fu      #param
                    ----------------------------------
                    angles      3       1       2
                    angles      3       2       2
                    angles      3       3       3
                    angles      3       4       4
                    angles      3       5       4
                    angles      3       6       6
                    angles      3       8       ??
                    '''

                    ai, aj , ak = fields[:3]
                    fu          = int(fields[3])
                    assert fu in (1,2,3,4,5,6,8)  # no 7

                    if fu not in (1,2,5):
                        raise NotImplementedError('function {0:d} is not yet supported'.format(fu))

                    ang = blocks.AngleType('gromacs')
                    if fu == 1:
                        if curr_sec == 'angletypes':
                            ang.atype1 = ai
                            ang.atype2 = aj
                            ang.atype3 = ak

                            tetha0, ktetha = list(map(float, fields[4:6]))
                            ang.gromacs = {'param':{'ktetha':ktetha, 'tetha0':tetha0, 'kub':None, 's0':None}, 'func':fu}

                            self.angletypes.append(ang)
                            _add_info(self, curr_sec, self.angletypes)

                        elif curr_sec == 'angles':
                            ai, aj, ak = list(map(int, [ai, aj, ak]))
                            ang.atom1 = mol.atoms[ai-1]
                            ang.atom2 = mol.atoms[aj-1]
                            ang.atom3 = mol.atoms[ak-1]
                            ang.gromacs['func'] = fu

                            mol.angles.append(ang)
                            _add_info(mol, curr_sec, mol.angles)

                        else:
                            raise ValueError

                    elif fu == 2:
                        if curr_sec == 'angletypes':
                            raise NotImplementedError()

                        elif curr_sec == 'angles':
                            ai, aj, ak = list(map(int, [ai, aj, ak]))
                            ang.atom1 = mol.atoms[ai-1]
                            ang.atom2 = mol.atoms[aj-1]
                            ang.atom3 = mol.atoms[ak-1]
                            ang.gromacs['func'] = fu

                            tetha0, ktetha = list(map(float, fields[4:6]))
                            ang.gromacs = {'param':{'ktetha':ktetha, 'tetha0':tetha0, 'kub':None, 's0':None}, 'func':fu}

                            mol.angles.append(ang)
                            _add_info(mol, curr_sec, mol.angles)

                    elif fu == 5:
                        if curr_sec == 'angletypes':
                            ang.atype1 = ai
                            ang.atype2 = aj
                            ang.atype3 = ak
                            tetha0, ktetha, s0, kub = list(map(float, fields[4:8]))

                            ang.gromacs = {'param':{'ktetha':ktetha, 'tetha0':tetha0, 'kub':kub, 's0':s0}, 'func':fu}

                            self.angletypes.append(ang)
                            _add_info(self, curr_sec, self.angletypes)

                        elif curr_sec == 'angles':
                            ai, aj, ak = list(map(int, [ai, aj, ak]))
                            ang.atom1 = mol.atoms[ai-1]
                            ang.atom2 = mol.atoms[aj-1]
                            ang.atom3 = mol.atoms[ak-1]
                            ang.gromacs['func'] = fu

                            mol.angles.append(ang)
                            _add_info(mol, curr_sec, mol.angles)

                        else:
                            raise ValueError

                    else:
                        raise NotImplementedError


                elif curr_sec in  ('dihedraltypes', 'dihedrals'):
                    '''
                    section     #at     fu      #param
                    ----------------------------------
                    dihedrals   4       1       3
                    dihedrals   4       2       2
                    dihedrals   4       3       6
                    dihedrals   4       4       3
                    dihedrals   4       5       4
                    dihedrals   4       8       ??
                    dihedrals   4       9       3
                    '''

                    if curr_sec == 'dihedraltypes' and len(fields) == 6:
                        # in oplsaa - quartz parameters
                        fields.insert(2, 'X')
                        fields.insert(0, 'X')

                    ai, aj, ak, am = fields[:4]
                    fu = int(fields[4])
                    assert fu in (1,2,3,4,5,8,9)

                    if fu not in (1,2,3,4,9):
                        raise NotImplementedError('dihedral function {0:d} is not yet supported'.format(fu))

                    dih = blocks.DihedralType('gromacs')
                    imp = blocks.ImproperType('gromacs')
                    # proper dihedrals
                    if fu in (1,3,9):
                        if curr_sec == 'dihedraltypes':
                            dih.atype1 = ai
                            dih.atype2 = aj
                            dih.atype3 = ak
                            dih.atype4 = am

                            dih.line = i_line + 1

                            if fu == 1:
                                delta, kchi, n = list(map(float, fields[5:8]))
                                dih.gromacs['param'].append({'kchi':kchi, 'n':n, 'delta':delta})
                            elif fu == 3:
                                c0, c1, c2, c3, c4, c5 = list(map(float, fields[5:11]))
                                m = dict(c0=c0, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5)
                                dih.gromacs['param'].append(m)
                            elif fu == 4:
                                delta, kchi, n = list(map(float, fields[5:8]))
                                dih.gromacs['param'].append({'kchi':kchi, 'n':int(n), 'delta':delta})
                            elif fu == 9:
                                delta, kchi, n = list(map(float, fields[5:8]))
                                dih.gromacs['param'].append({'kchi':kchi, 'n':int(n), 'delta':delta})
                            else:
                                raise ValueError

                            dih.gromacs['func'] = fu
                            self.dihedraltypes.append(dih)
                            _add_info(self, curr_sec, self.dihedraltypes)

                        elif curr_sec == 'dihedrals':
                            ai, aj, ak, am = list(map(int, fields[:4]))
                            dih.atom1 = mol.atoms[ai-1]
                            dih.atom2 = mol.atoms[aj-1]
                            dih.atom3 = mol.atoms[ak-1]
                            dih.atom4 = mol.atoms[am-1]
                            dih.gromacs['func'] = fu

                            dih.line = i_line + 1

                            if fu == 1:
                                delta, kchi, n = list(map(float, fields[5:8]))
                                dih.gromacs['param'].append({'kchi':kchi, 'n': int(n), 'delta':delta})
                            elif fu == 3:
                                pass
                            elif fu == 4:
                                pass
                            elif fu == 9:
                                if len(fields[5:8]) == 3:
                                    delta, kchi, n = list(map(float, fields[5:8]))
                                    dih.gromacs['param'].append({'kchi':kchi, 'n':int(n), 'delta':delta})
                            else:
                                raise ValueError

                            mol.dihedrals.append(dih)
                            _add_info(mol, curr_sec, mol.dihedrals)

                        else:
                            raise ValueError
                    # impropers
                    elif fu in (2,4):
                        if curr_sec == 'dihedraltypes':
                            imp.atype1 = ai
                            imp.atype2 = aj
                            imp.atype3 = ak
                            imp.atype4 = am

                            imp.line = i_line + 1

                            if fu == 2:
                                psi0 , kpsi = list(map(float, fields[5:7]))
                                imp.gromacs['param'].append({'kpsi':kpsi, 'psi0': psi0})
                            elif fu == 4:
                                psi0 , kpsi, n = list(map(float, fields[5:8]))
                                imp.gromacs['param'].append({'kpsi':kpsi, 'psi0': psi0, 'n': int(n)})
                            else:
                                raise ValueError

                            imp.gromacs['func'] = fu
                            self.impropertypes.append(imp)
                            _add_info(self, curr_sec, self.impropertypes)

                        elif curr_sec == 'dihedrals':
                            ai, aj, ak, am = list(map(int, fields[:4]))
                            imp.atom1 = mol.atoms[ai-1]
                            imp.atom2 = mol.atoms[aj-1]
                            imp.atom3 = mol.atoms[ak-1]
                            imp.atom4 = mol.atoms[am-1]
                            imp.gromacs['func'] = fu

                            imp.line = i_line + 1

                            if fu == 2:
                                pass
                            elif fu == 4:
                                # in-line override of dihedral parameters
                                if len(fields[5:8]) == 3:
                                    psi0 , kpsi, n = list(map(float, fields[5:8]))
                                    imp.gromacs['param'].append({'kpsi':kpsi, 'psi0': psi0, 'n': int(n)})
                            else:
                                raise ValueError

                            mol.impropers.append(imp)
                            _add_info(mol, curr_sec, mol.impropers)

                        else:
                            raise ValueError

                    else:
                        raise NotImplementedError


                elif curr_sec in ('cmaptypes', 'cmap'):

                    cmap = blocks.CMapType('gromacs')
                    if curr_sec == 'cmaptypes':
                        cmap_lines.append(line)
                        _add_info(self, curr_sec, self.cmaptypes)
                    else:
                        ai, aj, ak, am, an = list(map(int, fields[:5]))
                        fu = int(fields[5])
                        assert fu == 1
                        cmap.atom1 = mol.atoms[ai-1]
                        cmap.atom2 = mol.atoms[aj-1]
                        cmap.atom3 = mol.atoms[ak-1]
                        cmap.atom4 = mol.atoms[am-1]
                        cmap.atom8 = mol.atoms[an-1]
                        cmap.gromacs['func'] = fu

                        mol.cmaps.append(cmap)
                        _add_info(mol, curr_sec, mol.cmaps)


                elif curr_sec == 'settles':
                    '''
                    section     #at     fu      #param
                    ----------------------------------
                    '''

                    assert len(fields) == 4
                    ai = int(fields[0])
                    fu = int(fields[1])
                    assert fu == 1

                    settle = blocks.SettleType('gromacs')
                    settle.atom = mol.atoms[ai-1]
                    settle.dOH = float(fields[2])
                    settle.dHH = float(fields[3])

                    mol.settles.append(settle)
                    _add_info(mol, curr_sec, mol.settles)

                elif curr_sec == "virtual_sites3":
                    '''
                        ; Dummy from            funct   a       b
                        4   1   2   3   1   0.131937768 0.131937768
                    '''
                    assert len(fields) == 7
                    ai = int(fields[0])
                    aj = int(fields[1])
                    ak = int(fields[2])
                    al = int(fields[3])
                    fu = int(fields[4])
                    assert fu == 1
                    a = float(fields[5])
                    b = float(fields[6])

                    vs3 = blocks.VirtualSites3Type('gromacs')
                    vs3.atom1 = ai
                    vs3.atom2 = aj
                    vs3.atom3 = ak
                    vs3.atom4 = al
                    vs3.gromacs['func'] = fu
                    vs3.gromacs['param'] = { 'a': a, 'b':b }
                    mol.virtual_sites3.append(vs3)
                    _add_info(mol, curr_sec, mol.virtual_sites3)


                elif curr_sec in ('exclusions',):
                    ai = int(fields[0])
                    other = list(map(int, fields[1:]))

                    exc = blocks.Exclusion()
                    exc.main_atom  = mol.atoms[ai-1]
                    exc.other_atoms= [mol.atoms[k-1] for k in other]

                    mol.exclusions.append(exc)
                    _add_info(mol, curr_sec, mol.exclusions)


                elif curr_sec in ('constrainttypes', 'constraints'):
                    '''
                    section     #at     fu      #param
                    ----------------------------------
                    constraints 2       1       1
                    constraints 2       2       1
                    '''

                    ai, aj = fields[:2]
                    fu = int(fields[2])
                    assert fu in (1,2)

                    cons = blocks.ConstraintType('gromacs')

                    # TODO: what's different between 1 and 2
                    if fu in [1, 2]:
                        if curr_sec == 'constrainttypes':
                            cons.atype1 = ai
                            cons.atype2 = aj
                            b0 = float(fields[3])
                            cons.gromacs = {'param':{'b0':b0}, 'func': fu}

                            self.constrainttypes.append(cons)
                            _add_info(self, curr_sec, self.constrainttypes)

                        elif curr_sec == 'constraints':
                            ai, aj = list(map(int, fields[:2]))
                            cons.atom1 = mol.atoms[ai-1]
                            cons.atom2 = mol.atoms[aj-1]
                            cons.gromacs['func'] = fu

                            mol.constraints.append(cons)
                            _add_info(mol, curr_sec, mol.constraints)

                        else:
                            raise ValueError
                    else:
                        raise ValueError

                elif curr_sec in ('position_restraints',
                                  'distance_restraints',
                                  'dihedral_restraints',
                                  'orientation_restraints',
                                  'angle_restraints',
                                  'angle_restraints_z'):
                    pass


                elif curr_sec in ('implicit_genborn_params',):
                    '''
                    attype   sar     st      pi      gbr      hct
                    '''
                    pass

                elif curr_sec == 'system':
                    #assert len(fields) == 1
                    self.name = fields[0]


                elif curr_sec == 'molecules':
                    assert len(fields) == 2
                    mname, nmol = fields[0], int(fields[1])

                    # if the number of a molecule is more than 1, add copies to system.molecules
                    for i in range(nmol):
                        self.molecules.append(self.dict_molname_mol[mname])

                else:
                    raise NotImplementedError('Unknown section in topology: {0}'.format(curr_sec))

        # process cmap_lines
        curr_cons = None
        for line in cmap_lines:

            # cmaptype opening line
            if len(line.split()) == 8:
                cons = blocks.CMapType('gromacs')

                atype1, atype2, atype3, atype4, atype8, func, sizeX, sizeY = line.replace("\\","").split()
                func, sizeX, sizeY = int(func), int(sizeX), int(sizeY)
                cons.atype1 = atype1
                cons.atype2 = atype2
                cons.atype3 = atype3
                cons.atype4 = atype4
                cons.atype8 = atype8
                cons.gromacs = {'param':[], 'func': func}

                curr_cons = cons

            # cmap body
            elif len(line.split()) == 10:
                cmap_param = map(float, line.replace("\\","").split())
                cons.gromacs['param'] += cmap_param

            # cmaptype cloning line
            elif len(line.split()) == 6:
                cmap_param = map(float, line.replace("\\","").split())
                cons.gromacs['param'] += cmap_param
                self.cmaptypes.append(curr_cons)
            else:
                raise ValueError