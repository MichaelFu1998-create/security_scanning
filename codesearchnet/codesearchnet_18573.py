def run_program(prog_list, debug, shell):
    """Run a  program and check program return code Note that some commands don't work
    well with Popen.  So if this function is specifically called with 'shell=True',
    then it will run the old 'os.system'. In which case, there is no program output
    """
    try:
        if not shell:
            process = Popen(prog_list, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            retcode = process.returncode
            if debug >= 1:
                print("Program : ", " ".join(prog_list))
                print("Return Code: ", retcode)
                print("Stdout: ", stdout)
                print("Stderr: ", stderr)
            return bool(retcode)
        else:
            command = " ".join(prog_list)
            os.system(command)
            return True
    except:
        return False