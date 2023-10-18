def run(cmd):
    """
    Run a shell command
    """
    cmd = [pipes.quote(c) for c in cmd]
    cmd = " ".join(cmd)
    cmd += "; exit 0"
    # print("Running {} in {}".format(cmd, os.getcwd()))
    try:
        output = subprocess.check_output(cmd,
                                         stderr=subprocess.STDOUT,
                                         shell=True)
    except subprocess.CalledProcessError as e:
            output = e.output

    output = output.decode('utf-8')
    output = output.strip()
    return output