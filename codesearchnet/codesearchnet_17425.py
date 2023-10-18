def runEventLoop(argv=None, unexpectedErrorAlert=None, installInterrupt=None, pdb=None, main=NSApplicationMain):
    """Run the event loop, ask the user if we should continue if an
    exception is caught. Use this function instead of NSApplicationMain().
    """
    if argv is None:
        argv = sys.argv

    if pdb is None:
        pdb = 'USE_PDB' in os.environ

    if pdb:
        from PyObjCTools import Debugging
        Debugging.installVerboseExceptionHandler()
        # bring it to the front, starting from terminal
        # often won't
        activator = PyObjCAppHelperApplicationActivator_wrap.alloc().init()
        NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
            activator,
            'activateNow:',
            NSApplicationDidFinishLaunchingNotification,
            None,
        )
    else:
        Debugging = None

    if installInterrupt is None and pdb:
        installInterrupt = True

    if unexpectedErrorAlert is None:
        unexpectedErrorAlert = unexpectedErrorAlertPdb

    runLoop = NSRunLoop.currentRunLoop()
    stopper = PyObjCAppHelperRunLoopStopper_wrap.alloc().init()
    PyObjCAppHelperRunLoopStopper_wrap.addRunLoopStopper_toRunLoop_(stopper, runLoop)

    firstRun = NSApp() is None
    try:

        while stopper.shouldRun():
            try:
                if firstRun:
                    firstRun = False
                    if installInterrupt:
                        installMachInterrupt()
                    main(argv)
                else:
                    NSApp().run()
            except RAISETHESE:
                traceback.print_exc()
                break
            except:
                exctype, e, tb = sys.exc_info()
                objc_exception = False
                if isinstance(e, objc.error):
                    NSLog("%@", str(e))
                elif not unexpectedErrorAlert():
                    NSLog("%@", "An exception has occured:")
                    traceback.print_exc()
                    sys.exit(0)
                else:
                    NSLog("%@", "An exception has occured:")
                    traceback.print_exc()
            else:
                break

    finally:
        if Debugging is not None:
            Debugging.removeExceptionHandler()
        PyObjCAppHelperRunLoopStopper_wrap.removeRunLoopStopperFromRunLoop_(runLoop)