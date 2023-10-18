def take_snapshot(droplet, name):
    """
    Take a snapshot of a droplet

    Parameters
    ----------
    name: str
        name for snapshot
    """
    print "powering off"
    droplet.power_off()
    droplet.wait() # wait for pending actions to complete
    print "taking snapshot"
    droplet.take_snapshot(name)
    droplet.wait()
    snapshots = droplet.snapshots()
    print "Current snapshots"
    print snapshots