def WheelUp(wheelTimes: int = 1, interval: float = 0.05, waitTime: float = OPERATION_WAIT_TIME) -> None:
    """
    Simulate mouse wheel up.
    wheelTimes: int.
    interval: float.
    waitTime: float.
    """
    for i in range(wheelTimes):
        mouse_event(MouseEventFlag.Wheel, 0, 0, 120, 0) #WHEEL_DELTA=120
        time.sleep(interval)
    time.sleep(waitTime)