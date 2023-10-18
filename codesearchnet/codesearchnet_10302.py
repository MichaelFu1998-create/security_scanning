def remove_molecules_from_topology(filename, **kwargs):
    """Remove autogenerated [ molecules ] entries from *filename*.

    Valid entries in ``[ molecules ]`` below the default *marker*
    are removed. For example, a topology file such as ::

       [ molecules ]
       Protein    1
       SOL      213
       ; The next line is the marker!
       ; Gromacs auto-generated entries follow:
       SOL            12345
       NA+     15
       CL-      16
       ; This is a comment that is NOT deleted.
       SOL            333

    would become::

       [ molecules ]
       Protein    1
       SOL      213
       ; The next line is the marker!
       ; Gromacs auto-generated entries follow:
       ; This is a comment that is NOT deleted.

    Valid molecule lines look like ``SOL 1234``, ``NA 17`` etc. The
    actual regular expression used is "\s*[\w+_-]+\s+\d+\s*(;.*)?$".

    In order to use this function, the marker line has to be manually
    added to the topology file.

    :Arguments:
      *filename*
         The topology file that includes the  ``[ molecules ]`` section.
         It is **edited in place**.
      *marker*
         Any ``[ molecules ]`` entries below this pattern (python regular
         expression) are removed. Leading white space is ignored. ``None``
         uses the default as described above.
    """
    marker = kwargs.pop('marker', None)
    if marker is None:
        marker = "; Gromacs auto-generated entries follow:"
    logger.debug("Scrubbed [ molecules ]: marker = %(marker)r", vars())

    p_marker = re.compile("\s*{0!s}".format(marker))
    p_molecule = re.compile("\s*[\w+_-]+\s+\d+\s*(;.*)?$")
    with tempfile.TemporaryFile() as target:
        with open(filename, 'rb') as src:
            autogenerated = False
            n_removed = 0
            for line in src:
                line = line.decode('utf-8')
                if p_marker.match(line):
                    autogenerated = True
                if autogenerated and p_molecule.match(line):
                    n_removed += 1
                    continue  # remove by skipping
                target.write(line.encode('utf-8'))
        if autogenerated and n_removed > 0:
            target.seek(0)
            with open(filename, 'wb') as final:   # overwrite original!
                shutil.copyfileobj(target, final)
            logger.info("Removed %(n_removed)d autogenerated [ molecules ] from "
                        "topol = %(filename)r" % vars())
    return n_removed