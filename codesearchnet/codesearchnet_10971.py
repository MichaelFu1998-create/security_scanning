def init(window=None, project=None, timeline=None):
    """
    Initialize, load and run

    :param manager: The effect manager to use
    """
    from demosys.effects.registry import Effect
    from demosys.scene import camera

    window.timeline = timeline

    # Inject attributes into the base Effect class
    setattr(Effect, '_window', window)
    setattr(Effect, '_ctx', window.ctx)
    setattr(Effect, '_project', project)

    # Set up the default system camera
    window.sys_camera = camera.SystemCamera(aspect=window.aspect_ratio, fov=60.0, near=1, far=1000)
    setattr(Effect, '_sys_camera', window.sys_camera)

    print("Loading started at", time.time())
    project.load()

    # Initialize timer
    timer_cls = import_string(settings.TIMER)
    window.timer = timer_cls()
    window.timer.start()