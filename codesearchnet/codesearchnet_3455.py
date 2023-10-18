def symbolic_run_get_cons(trace):
    '''
    Execute a symbolic run that follows a concrete run; return constraints generated
    and the stdin data produced
    '''

    m2 = Manticore.linux(prog, workspace_url='mem:')
    f = Follower(trace)
    m2.verbosity(VERBOSITY)
    m2.register_plugin(f)

    def on_term_testcase(mcore, state, stateid, err):
        with m2.locked_context() as ctx:
            readdata = []
            for name, fd, data in state.platform.syscall_trace:
                if name in ('_receive', '_read') and fd == 0:
                    readdata.append(data)
            ctx['readdata'] = readdata
            ctx['constraints'] = list(state.constraints.constraints)

    m2.subscribe('will_terminate_state', on_term_testcase)

    m2.run()

    constraints = m2.context['constraints']
    datas = m2.context['readdata']

    return constraints, datas