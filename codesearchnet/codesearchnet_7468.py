def compile(self, *mibnames, **options):
        """Transform requested and possibly referred MIBs.

        The *compile* method should be invoked when *MibCompiler* object
        is operational meaning at least *sources* are specified.

        Once called with a MIB module name, *compile* will:

        * fetch ASN.1 MIB module with given name by calling *sources*
        * make sure no such transformed MIB already exists (with *searchers*)
        * parse ASN.1 MIB text with *parser*
        * perform actual MIB transformation into target format with *code generator*
        * may attempt to borrow pre-transformed MIB through *borrowers*
        * write transformed MIB through *writer*

        The above sequence will be performed for each MIB name given in
        *mibnames* and may be performed for all MIBs referred to from
        MIBs being processed.

        Args:
            mibnames: list of ASN.1 MIBs names
            options: options that affect the way PySMI components work

        Returns:
            A dictionary of MIB module names processed (keys) and *MibStatus*
            class instances (values)

        """
        processed = {}
        parsedMibs = {}
        failedMibs = {}
        borrowedMibs = {}
        builtMibs = {}
        symbolTableMap = {}
        mibsToParse = [x for x in mibnames]
        canonicalMibNames = {}

        while mibsToParse:
            mibname = mibsToParse.pop(0)

            if mibname in parsedMibs:
                debug.logger & debug.flagCompiler and debug.logger('MIB %s already parsed' % mibname)
                continue

            if mibname in failedMibs:
                debug.logger & debug.flagCompiler and debug.logger('MIB %s already failed' % mibname)
                continue

            for source in self._sources:
                debug.logger & debug.flagCompiler and debug.logger('trying source %s' % source)

                try:
                    fileInfo, fileData = source.getData(mibname)

                    for mibTree in self._parser.parse(fileData):
                        mibInfo, symbolTable = self._symbolgen.genCode(
                            mibTree, symbolTableMap
                        )

                        symbolTableMap[mibInfo.name] = symbolTable

                        parsedMibs[mibInfo.name] = fileInfo, mibInfo, mibTree

                        if mibname in failedMibs:
                            del failedMibs[mibname]

                        mibsToParse.extend(mibInfo.imported)

                        if fileInfo.name in mibnames:
                            if mibInfo.name not in canonicalMibNames:
                                canonicalMibNames[mibInfo.name] = []
                            canonicalMibNames[mibInfo.name].append(fileInfo.name)

                        debug.logger & debug.flagCompiler and debug.logger(
                            '%s (%s) read from %s, immediate dependencies: %s' % (
                                mibInfo.name, mibname, fileInfo.path, ', '.join(mibInfo.imported) or '<none>'))

                    break

                except error.PySmiReaderFileNotFoundError:
                    debug.logger & debug.flagCompiler and debug.logger('no %s found at %s' % (mibname, source))
                    continue

                except error.PySmiError:
                    exc_class, exc, tb = sys.exc_info()
                    exc.source = source
                    exc.mibname = mibname
                    exc.msg += ' at MIB %s' % mibname

                    debug.logger & debug.flagCompiler and debug.logger('%serror %s from %s' % (
                        options.get('ignoreErrors') and 'ignoring ' or 'failing on ', exc, source))

                    failedMibs[mibname] = exc

                    processed[mibname] = statusFailed.setOptions(error=exc)

            else:
                exc = error.PySmiError('MIB source %s not found' % mibname)
                exc.mibname = mibname
                debug.logger & debug.flagCompiler and debug.logger('no %s found everywhere' % mibname)

                if mibname not in failedMibs:
                    failedMibs[mibname] = exc

                if mibname not in processed:
                    processed[mibname] = statusMissing

        debug.logger & debug.flagCompiler and debug.logger(
            'MIBs analyzed %s, MIBs failed %s' % (len(parsedMibs), len(failedMibs)))

        #
        # See what MIBs need generating
        #

        for mibname in tuple(parsedMibs):
            fileInfo, mibInfo, mibTree = parsedMibs[mibname]

            debug.logger & debug.flagCompiler and debug.logger('checking if %s requires updating' % mibname)

            for searcher in self._searchers:
                try:
                    searcher.fileExists(mibname, fileInfo.mtime, rebuild=options.get('rebuild'))

                except error.PySmiFileNotFoundError:
                    debug.logger & debug.flagCompiler and debug.logger(
                        'no compiled MIB %s available through %s' % (mibname, searcher))
                    continue

                except error.PySmiFileNotModifiedError:
                    debug.logger & debug.flagCompiler and debug.logger(
                        'will be using existing compiled MIB %s found by %s' % (mibname, searcher))
                    del parsedMibs[mibname]
                    processed[mibname] = statusUntouched
                    break

                except error.PySmiError:
                    exc_class, exc, tb = sys.exc_info()
                    exc.searcher = searcher
                    exc.mibname = mibname
                    exc.msg += ' at MIB %s' % mibname
                    debug.logger & debug.flagCompiler and debug.logger('error from %s: %s' % (searcher, exc))
                    continue

            else:
                debug.logger & debug.flagCompiler and debug.logger(
                    'no suitable compiled MIB %s found anywhere' % mibname)

                if options.get('noDeps') and mibname not in canonicalMibNames:
                    debug.logger & debug.flagCompiler and debug.logger(
                        'excluding imported MIB %s from code generation' % mibname)
                    del parsedMibs[mibname]
                    processed[mibname] = statusUntouched
                    continue

        debug.logger & debug.flagCompiler and debug.logger(
            'MIBs parsed %s, MIBs failed %s' % (len(parsedMibs), len(failedMibs)))

        #
        # Generate code for parsed MIBs
        #

        for mibname in parsedMibs.copy():
            fileInfo, mibInfo, mibTree = parsedMibs[mibname]

            debug.logger & debug.flagCompiler and debug.logger('compiling %s read from %s' % (mibname, fileInfo.path))

            platform_info, user_info = self._get_system_info()

            comments = [
                'ASN.1 source %s' % fileInfo.path,
                'Produced by %s-%s at %s' % (packageName, packageVersion, time.asctime()),
                'On host %s platform %s version %s by user %s' % (platform_info[1], platform_info[0],
                                                                  platform_info[2], user_info[0]),
                'Using Python version %s' % sys.version.split('\n')[0]
            ]

            try:
                mibInfo, mibData = self._codegen.genCode(
                    mibTree,
                    symbolTableMap,
                    comments=comments,
                    dstTemplate=options.get('dstTemplate'),
                    genTexts=options.get('genTexts'),
                    textFilter=options.get('textFilter')
                )

                builtMibs[mibname] = fileInfo, mibInfo, mibData
                del parsedMibs[mibname]

                debug.logger & debug.flagCompiler and debug.logger(
                    '%s read from %s and compiled by %s' % (mibname, fileInfo.path, self._writer))

            except error.PySmiError:
                exc_class, exc, tb = sys.exc_info()
                exc.handler = self._codegen
                exc.mibname = mibname
                exc.msg += ' at MIB %s' % mibname

                debug.logger & debug.flagCompiler and debug.logger('error from %s: %s' % (self._codegen, exc))

                processed[mibname] = statusFailed.setOptions(error=exc)

                failedMibs[mibname] = exc
                del parsedMibs[mibname]

        debug.logger & debug.flagCompiler and debug.logger(
            'MIBs built %s, MIBs failed %s' % (len(parsedMibs), len(failedMibs)))

        #
        # Try to borrow pre-compiled MIBs for failed ones
        #

        for mibname in failedMibs.copy():
            if options.get('noDeps') and mibname not in canonicalMibNames:
                debug.logger & debug.flagCompiler and debug.logger('excluding imported MIB %s from borrowing' % mibname)
                continue

            for borrower in self._borrowers:
                debug.logger & debug.flagCompiler and debug.logger('trying to borrow %s from %s' % (mibname, borrower))
                try:
                    fileInfo, fileData = borrower.getData(
                        mibname,
                        genTexts=options.get('genTexts')
                    )

                    borrowedMibs[mibname] = fileInfo, MibInfo(name=mibname, imported=[]), fileData

                    del failedMibs[mibname]

                    debug.logger & debug.flagCompiler and debug.logger('%s borrowed with %s' % (mibname, borrower))
                    break

                except error.PySmiError:
                    debug.logger & debug.flagCompiler and debug.logger('error from %s: %s' % (borrower, sys.exc_info()[1]))

        debug.logger & debug.flagCompiler and debug.logger(
            'MIBs available for borrowing %s, MIBs failed %s' % (len(borrowedMibs), len(failedMibs)))

        #
        # See what MIBs need borrowing
        #

        for mibname in borrowedMibs.copy():
            debug.logger & debug.flagCompiler and debug.logger('checking if failed MIB %s requires borrowing' % mibname)

            fileInfo, mibInfo, mibData = borrowedMibs[mibname]

            for searcher in self._searchers:
                try:
                    searcher.fileExists(mibname, fileInfo.mtime, rebuild=options.get('rebuild'))

                except error.PySmiFileNotFoundError:
                    debug.logger & debug.flagCompiler and debug.logger(
                        'no compiled MIB %s available through %s' % (mibname, searcher))
                    continue

                except error.PySmiFileNotModifiedError:
                    debug.logger & debug.flagCompiler and debug.logger(
                        'will be using existing compiled MIB %s found by %s' % (mibname, searcher))
                    del borrowedMibs[mibname]
                    processed[mibname] = statusUntouched
                    break

                except error.PySmiError:
                    exc_class, exc, tb = sys.exc_info()
                    exc.searcher = searcher
                    exc.mibname = mibname
                    exc.msg += ' at MIB %s' % mibname

                    debug.logger & debug.flagCompiler and debug.logger('error from %s: %s' % (searcher, exc))

                    continue
            else:
                debug.logger & debug.flagCompiler and debug.logger(
                    'no suitable compiled MIB %s found anywhere' % mibname)

                if options.get('noDeps') and mibname not in canonicalMibNames:
                    debug.logger & debug.flagCompiler and debug.logger(
                        'excluding imported MIB %s from borrowing' % mibname)
                    processed[mibname] = statusUntouched

                else:
                    debug.logger & debug.flagCompiler and debug.logger('will borrow MIB %s' % mibname)
                    builtMibs[mibname] = borrowedMibs[mibname]

                    processed[mibname] = statusBorrowed.setOptions(
                        path=fileInfo.path, file=fileInfo.file,
                        alias=fileInfo.name
                    )

                del borrowedMibs[mibname]

        debug.logger & debug.flagCompiler and debug.logger(
            'MIBs built %s, MIBs failed %s' % (len(builtMibs), len(failedMibs)))

        #
        # We could attempt to ignore missing/failed MIBs
        #

        if failedMibs and not options.get('ignoreErrors'):
            debug.logger & debug.flagCompiler and debug.logger('failing with problem MIBs %s' % ', '.join(failedMibs))

            for mibname in builtMibs:
                processed[mibname] = statusUnprocessed

            return processed

        debug.logger & debug.flagCompiler and debug.logger(
            'proceeding with built MIBs %s, failed MIBs %s' % (', '.join(builtMibs), ', '.join(failedMibs)))

        #
        # Store compiled MIBs
        #

        for mibname in builtMibs.copy():
            fileInfo, mibInfo, mibData = builtMibs[mibname]

            try:
                if options.get('writeMibs', True):
                    self._writer.putData(
                        mibname, mibData, dryRun=options.get('dryRun')
                    )

                debug.logger & debug.flagCompiler and debug.logger('%s stored by %s' % (mibname, self._writer))

                del builtMibs[mibname]

                if mibname not in processed:
                    processed[mibname] = statusCompiled.setOptions(
                        path=fileInfo.path,
                        file=fileInfo.file,
                        alias=fileInfo.name,
                        oid=mibInfo.oid,
                        oids=mibInfo.oids,
                        identity=mibInfo.identity,
                        revision=mibInfo.revision,
                        enterprise=mibInfo.enterprise,
                        compliance=mibInfo.compliance,
                    )

            except error.PySmiError:
                exc_class, exc, tb = sys.exc_info()
                exc.handler = self._codegen
                exc.mibname = mibname
                exc.msg += ' at MIB %s' % mibname

                debug.logger & debug.flagCompiler and debug.logger('error %s from %s' % (exc, self._writer))

                processed[mibname] = statusFailed.setOptions(error=exc)
                failedMibs[mibname] = exc
                del builtMibs[mibname]

        debug.logger & debug.flagCompiler and debug.logger(
            'MIBs modified: %s' % ', '.join([x for x in processed if processed[x] in ('compiled', 'borrowed')]))

        return processed