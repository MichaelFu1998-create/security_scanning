def from_datafile(hash_, path='./', ignore_timestamps=False, mode='r'):
        """Load simulation from disk trajectories and (when present) timestamps.
        """
        path = Path(path)
        assert path.exists()

        file_traj = ParticlesSimulation.datafile_from_hash(
            hash_, prefix=ParticlesSimulation._PREFIX_TRAJ, path=path)
        store = TrajectoryStore(file_traj, mode='r')

        psf_pytables = store.h5file.get_node('/psf/default_psf')
        psf = NumericPSF(psf_pytables=psf_pytables)
        box = store.h5file.get_node_attr('/parameters', 'box')
        P = store.h5file.get_node_attr('/parameters', 'particles')

        names = ['t_step', 't_max', 'EID', 'ID']
        kwargs = {name: store.numeric_params[name] for name in names}
        S = ParticlesSimulation(particles=Particles.from_json(P), box=box,
                                psf=psf, **kwargs)

        # Emulate S.open_store_traj()
        S.store = store
        S.psf_pytables = psf_pytables
        S.traj_group = S.store.h5file.root.trajectories
        S.emission = S.traj_group.emission
        S.emission_tot = S.traj_group.emission_tot
        if 'position' in S.traj_group:
            S.position = S.traj_group.position
        elif 'position_rz' in S.traj_group:
            S.position = S.traj_group.position_rz
        S.chunksize = S.store.h5file.get_node('/parameters', 'chunksize')
        if not ignore_timestamps:
            try:
                file_ts = ParticlesSimulation.datafile_from_hash(
                    hash_, prefix=ParticlesSimulation._PREFIX_TS, path=path)
            except NoMatchError:
                # There are no timestamps saved.
                pass
            else:
                # Load the timestamps
                S.ts_store = TimestampStore(file_ts, mode=mode)
                S.ts_group = S.ts_store.h5file.root.timestamps
                print(' - Found matching timestamps.')
        return S