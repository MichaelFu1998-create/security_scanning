def build_swig():
    '''Run SWIG with specified parameters'''
    print("Looking for FANN libs...")
    find_fann()
    print("running SWIG...")
    swig_bin = find_swig()
    swig_cmd = [swig_bin, '-c++', '-python', 'fann2/fann2.i']
    subprocess.Popen(swig_cmd).wait()