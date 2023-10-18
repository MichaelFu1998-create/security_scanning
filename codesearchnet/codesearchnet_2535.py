def extract_scheduler_location(self, topology):
    """
    Returns the representation of scheduler location that will
    be returned from Tracker.
    """
    schedulerLocation = {
        "name": None,
        "http_endpoint": None,
        "job_page_link": None,
    }

    if topology.scheduler_location:
      schedulerLocation["name"] = topology.scheduler_location.topology_name
      schedulerLocation["http_endpoint"] = topology.scheduler_location.http_endpoint
      schedulerLocation["job_page_link"] = \
          topology.scheduler_location.job_page_link[0] \
          if len(topology.scheduler_location.job_page_link) > 0 else ""

    return schedulerLocation