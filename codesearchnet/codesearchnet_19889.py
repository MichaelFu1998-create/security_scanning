def update(self, tids, info):
        """
        Called to update the state of the iterator.  This methods
        receives the set of task ids from the previous set of tasks
        together with the launch information to allow the output
        values to be parsed using the output_extractor. This data is then
        used to determine the next desired point in the parameter
        space by calling the _update_state method.
        """
        outputs_dir = os.path.join(info['root_directory'], 'streams')
        pattern = '%s_*_tid_*{tid}.o.{tid}*' % info['batch_name']
        flist = os.listdir(outputs_dir)
        try:
            outputs = []
            for tid in tids:
                matches = fnmatch.filter(flist, pattern.format(tid=tid))
                if len(matches) != 1:
                    self.warning("No unique output file for tid %d" % tid)
                contents = open(os.path.join(outputs_dir, matches[0]),'r').read()
                outputs.append(self.output_extractor(contents))

            self._next_val = self._update_state(outputs)
            self.trace.append((outputs, self._next_val))
        except:
            self.warning("Cannot load required output files. Cannot continue.")
            self._next_val = StopIteration