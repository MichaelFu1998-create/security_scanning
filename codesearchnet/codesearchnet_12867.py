def run(self, steps=0, force=False, ipyclient=None, 
        show_cluster=0, **kwargs):
        """
        Run assembly steps of an ipyrad analysis. Enter steps as a string,
        e.g., "1", "123", "12345". This step checks for an existing
        ipcluster instance otherwise it raises an exception. The ipyparallel
        connection is made using information from the _ipcluster dict of the
        Assembly class object.
        """
        ## check that mindepth params are compatible, fix and report warning.
        self._compatible_params_check()

        ## wrap everything in a try statement to ensure that we save the
        ## Assembly object if it is interrupted at any point, and also
        ## to ensure proper cleanup of the ipyclient.
        inst = None
        try:
            ## use an existing ipcluster instance
            if not ipyclient:
                args = self._ipcluster.items() + [("spacer", self._spacer)]
                ipyclient = ip.core.parallel.get_client(**dict(args))

            ## print a message about the cluster status
            ## if MPI setup then we are going to wait until all engines are
            ## ready so that we can print how many cores started on each
            ## host machine exactly.
            if (self._cli) or show_cluster:
                ip.cluster_info(ipyclient=ipyclient, spacer=self._spacer)

            ## get the list of steps to run
            if isinstance(steps, int):
                steps = str(steps)
            steps = sorted(list(steps))

            ## print an Assembly name header if inside API
            if not self._cli:
                print("Assembly: {}".format(self.name))

            ## store ipyclient engine pids to the Assembly so we can 
            ## hard-interrupt them later if assembly is interrupted. 
            ## Only stores pids of engines that aren't busy at this moment, 
            ## otherwise it would block here while waiting to find their pids.
            self._ipcluster["pids"] = {}
            for eid in ipyclient.ids:
                engine = ipyclient[eid]
                if not engine.outstanding:
                    pid = engine.apply(os.getpid).get()
                    self._ipcluster["pids"][eid] = pid
            #ipyclient[:].apply(os.getpid).get_dict()

            ## has many fixed arguments right now, but we may add these to
            ## hackerz_only, or they may be accessed in the API.
            if '1' in steps:
                self._step1func(force, ipyclient)
                self.save()
                ipyclient.purge_everything()

            if '2' in steps:
                self._step2func(samples=None, force=force, ipyclient=ipyclient)
                self.save()
                ipyclient.purge_everything()

            if '3' in steps:
                self._step3func(samples=None, noreverse=0, force=force,
                             maxindels=8, ipyclient=ipyclient)
                self.save()
                ipyclient.purge_everything()

            if '4' in steps:
                self._step4func(samples=None, force=force, ipyclient=ipyclient)
                self.save()
                ipyclient.purge_everything()

            if '5' in steps:
                self._step5func(samples=None, force=force, ipyclient=ipyclient)
                self.save()
                ipyclient.purge_everything()

            if '6' in steps:
                self._step6func(samples=None, noreverse=0, randomseed=12345,
                                force=force, ipyclient=ipyclient, **kwargs)
                self.save()
                ipyclient.purge_everything()

            if '7' in steps:
                self._step7func(samples=None, force=force, ipyclient=ipyclient)
                self.save()
                ipyclient.purge_everything()


        ## handle exceptions so they will be raised after we clean up below
        except KeyboardInterrupt as inst:
            print("\n  Keyboard Interrupt by user")
            LOGGER.info("assembly interrupted by user.")

        except IPyradWarningExit as inst:
            LOGGER.error("IPyradWarningExit: %s", inst)
            print("\n  Encountered an error (see details in ./ipyrad_log.txt)"+\
                  "\n  Error summary is below -------------------------------"+\
                  "\n{}".format(inst))

        except Exception as inst:
            LOGGER.error(inst)
            print("\n  Encountered an unexpected error (see ./ipyrad_log.txt)"+\
                  "\n  Error message is below -------------------------------"+\
                  "\n{}".format(inst))

        ## close client when done or interrupted
        finally:
            try:
                ## save the Assembly
                self.save()

                ## can't close client if it was never open
                if ipyclient:

                    ## send SIGINT (2) to all engines
                    try:
                        ipyclient.abort()
                        time.sleep(1)
                        for engine_id, pid in self._ipcluster["pids"].items():
                            if ipyclient.queue_status()[engine_id]["tasks"]:
                                os.kill(pid, 2)
                                LOGGER.info('interrupted engine {} w/ SIGINT to {}'\
                                        .format(engine_id, pid))
                        time.sleep(1)
                    except ipp.NoEnginesRegistered:
                        pass

                    ## if CLI, stop jobs and shutdown. Don't use _cli here 
                    ## because you can have a CLI object but use the --ipcluster
                    ## flag, in which case we don't want to kill ipcluster.
                    if 'ipyrad-cli' in self._ipcluster["cluster_id"]:
                        LOGGER.info("  shutting down engines")
                        ipyclient.shutdown(hub=True, block=False)
                        ipyclient.close()
                        LOGGER.info("  finished shutdown")
                    else:
                        if not ipyclient.outstanding:
                            ipyclient.purge_everything()
                        else:
                            ## nanny: kill everything, something bad happened
                            ipyclient.shutdown(hub=True, block=False)
                            ipyclient.close()
                            print("\nwarning: ipcluster shutdown and must be restarted")
                    
            ## if exception is close and save, print and ignore
            except Exception as inst2:
                print("warning: error during shutdown:\n{}".format(inst2))
                LOGGER.error("shutdown warning: %s", inst2)