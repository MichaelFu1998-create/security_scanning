def get():
    """ Get the instance of the ClientJobsDAO created for this process (or
    perhaps at some point in the future, for this thread).

    Parameters:
    ----------------------------------------------------------------
    retval:  instance of ClientJobsDAO
    """

    # Instantiate if needed
    if ClientJobsDAO._instance is None:
      cjDAO = ClientJobsDAO()
      cjDAO.connect()

      ClientJobsDAO._instance = cjDAO

    # Return the instance to the caller
    return ClientJobsDAO._instance