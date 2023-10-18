def show(self, args, file_handle=None, **kwargs):
        "Write to file_handle if supplied, othewise print output"
        full_string = ''
        info = {'root_directory':     '<root_directory>',
                'batch_name':         '<batch_name>',
                'batch_tag':          '<batch_tag>',
                'batch_description':  '<batch_description>',
                'launcher':        '<launcher>',
                'timestamp_format':   '<timestamp_format>',
                'timestamp':          tuple(time.localtime()),
                'varying_keys':       args.varying_keys,
                'constant_keys':      args.constant_keys,
                'constant_items':     args.constant_items}

        quoted_cmds = [ subprocess.list2cmdline(
                [el for el in self(self._formatter(s),'<tid>',info)])
                        for s in args.specs]

        cmd_lines = ['%d: %s\n' % (i, qcmds) for (i,qcmds)
                     in enumerate(quoted_cmds)]
        full_string += ''.join(cmd_lines)
        if file_handle:
            file_handle.write(full_string)
            file_handle.flush()
        else:
            print(full_string)