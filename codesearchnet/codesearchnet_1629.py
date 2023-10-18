def retrySQL(timeoutSec=60*5, logger=None):
  """ Return a closure suitable for use as a decorator for
  retrying a pymysql DAO function on certain failures that warrant retries (
  e.g., RDS/MySQL server down temporarily, transaction deadlock, etc.).
  We share this function across multiple scripts (e.g., ClientJobsDAO,
  StreamMgr) for consitent behavior.

  .. note:: Please ensure that the operation being retried is idempotent.

  .. note:: logging must be initialized *before* any loggers are created, else
     there will be no output; see nupic.support.initLogging()

  Usage Example:

  .. code-block:: python

    @retrySQL()
    def jobInfo(self, jobID):
        ...

  :param timeoutSec:       How many seconds from time of initial call to stop retrying
                     (floating point)
  :param logger:           User-supplied logger instance.

  """

  if logger is None:
    logger = logging.getLogger(__name__)

  def retryFilter(e, args, kwargs):

    if isinstance(e, (pymysql.InternalError, pymysql.OperationalError)):
      if e.args and e.args[0] in _ALL_RETRIABLE_ERROR_CODES:
        return True

    elif isinstance(e, pymysql.Error):
      if (e.args and
          inspect.isclass(e.args[0]) and issubclass(e.args[0], socket_error)):
        return True

    return False


  retryExceptions = tuple([
    pymysql.InternalError,
    pymysql.OperationalError,
    pymysql.Error,
  ])

  return make_retry_decorator(
    timeoutSec=timeoutSec, initialRetryDelaySec=0.1, maxRetryDelaySec=10,
    retryExceptions=retryExceptions, retryFilter=retryFilter,
    logger=logger)