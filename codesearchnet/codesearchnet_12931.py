def count_seeds(usort):
    """
    uses bash commands to quickly count N seeds from utemp file
    """
    with open(usort, 'r') as insort:
        cmd1 = ["cut", "-f", "2"]
        cmd2 = ["uniq"]
        cmd3 = ["wc"]
        proc1 = sps.Popen(cmd1, stdin=insort, stdout=sps.PIPE, close_fds=True)
        proc2 = sps.Popen(cmd2, stdin=proc1.stdout, stdout=sps.PIPE, close_fds=True)
        proc3 = sps.Popen(cmd3, stdin=proc2.stdout, stdout=sps.PIPE, close_fds=True)
        res = proc3.communicate()
        nseeds = int(res[0].split()[0])
        proc1.stdout.close()
        proc2.stdout.close()
        proc3.stdout.close()
    return nseeds