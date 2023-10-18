def pex(ctx, pyrun='', upload=False, opts=''):
    """Package the project with PEX."""
    cfg = config.load()

    # Build and check release
    ctx.run(": invoke clean --all build test check")

    # Get full version
    pkg_info = get_egg_info(cfg)
    # from pprint import pprint; pprint(dict(pkg_info))
    version = pkg_info.version if pkg_info else cfg.project.version

    # Build a PEX for each console entry-point
    pex_files = []
    # from pprint import pprint; pprint(cfg.project.entry_points)
    for script in cfg.project.entry_points['console_scripts']:
        script, entry_point = script.split('=', 1)
        script, entry_point = script.strip(), entry_point.strip()
        pex_file = cfg.rootjoin('bin', '{}-{}.pex'.format(script, version))
        cmd = ['pex', '-r', cfg.rootjoin('requirements.txt'), cfg.project_root, '-c', script, '-o', pex_file]
        if opts:
            cmd.append(opts)
        ctx.run(' '.join(cmd))

        # Warn about non-portable stuff
        non_universal = set()
        with closing(zipfile.ZipFile(pex_file, mode="r")) as pex_contents:
            for pex_name in pex_contents.namelist():  # pylint: disable=no-member
                if pex_name.endswith('WHEEL') and '-py2.py3-none-any.whl' not in pex_name:
                    non_universal.add(pex_name.split('.whl')[0].split('/')[-1])
        if non_universal:
            notify.warning("Non-universal or native wheels in PEX '{}':\n    {}"
                           .format(pex_file.replace(os.getcwd(), '.'), '\n    '.join(sorted(non_universal))))
            envs = [i.split('-')[-3:] for i in non_universal]
            envs = {i[0]: i[1:] for i in envs}
            if len(envs) > 1:
                envs = {k: v for k, v in envs.items() if not k.startswith('py')}
            env_id = []
            for k, v in sorted(envs.items()):
                env_id.append(k)
                env_id.extend(v)
            env_id = '-'.join(env_id)
        else:
            env_id = 'py2.py3-none-any'

        new_pex_file = pex_file.replace('.pex', '-{}.pex'.format(env_id))
        notify.info("Renamed PEX to '{}'".format(os.path.basename(new_pex_file)))
        os.rename(pex_file, new_pex_file)
        pex_file = new_pex_file
        pex_files.append(pex_file)

    if not pex_files:
        notify.warning("No entry points found in project configuration!")
    else:
        if pyrun:
            if any(pyrun.startswith(i) for i in ('http://', 'https://', 'file://')):
                pyrun_url = pyrun
            else:
                pyrun_cfg = dict(ctx.rituals.pyrun)
                pyrun_cfg.update(parse_qsl(pyrun.replace(os.pathsep, '&')))
                pyrun_url = (pyrun_cfg['base_url'] + '/' +
                             pyrun_cfg['archive']).format(**pyrun_cfg)

            notify.info("Getting PyRun from '{}'...".format(pyrun_url))
            with url_as_file(pyrun_url, ext='tgz') as pyrun_tarball:
                pyrun_tar = tarfile.TarFile.gzopen(pyrun_tarball)
                for pex_file in pex_files[:]:
                    pyrun_exe = pyrun_tar.extractfile('./bin/pyrun')
                    with open(pex_file, 'rb') as pex_handle:
                        pyrun_pex_file = '{}{}-installer.sh'.format(
                            pex_file[:-4], pyrun_url.rsplit('/egenix')[-1][:-4])
                        with open(pyrun_pex_file, 'wb') as pyrun_pex:
                            pyrun_pex.write(INSTALLER_BASH.replace('00000', '{:<5d}'.format(len(INSTALLER_BASH) + 1)))
                            shutil.copyfileobj(pyrun_exe, pyrun_pex)
                            shutil.copyfileobj(pex_handle, pyrun_pex)
                        shutil.copystat(pex_file, pyrun_pex_file)
                        notify.info("Wrote PEX installer to '{}'".format(pretty_path(pyrun_pex_file)))
                        pex_files.append(pyrun_pex_file)

        if upload:
            base_url = ctx.rituals.release.upload.base_url.rstrip('/')
            if not base_url:
                notify.failure("No base URL provided for uploading!")

            for pex_file in pex_files:
                url = base_url + '/' + ctx.rituals.release.upload.path.lstrip('/').format(
                    name=cfg.project.name, version=cfg.project.version, filename=os.path.basename(pex_file))
                notify.info("Uploading to '{}'...".format(url))
                with io.open(pex_file, 'rb') as handle:
                    reply = requests.put(url, data=handle.read())
                    if reply.status_code in range(200, 300):
                        notify.info("{status_code} {reason}".format(**vars(reply)))
                    else:
                        notify.warning("{status_code} {reason}".format(**vars(reply)))