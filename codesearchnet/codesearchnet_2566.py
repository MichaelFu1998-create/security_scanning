def create_execution_state(self, topologyName, executionState):
    """ create execution state """
    if not executionState or not executionState.IsInitialized():
      raise_(StateException("Execution State protobuf not init properly",
                            StateException.EX_TYPE_PROTOBUF_ERROR), sys.exc_info()[2])

    path = self.get_execution_state_path(topologyName)
    LOG.info("Adding topology: {0} to path: {1}".format(
        topologyName, path))
    executionStateString = executionState.SerializeToString()
    try:
      self.client.create(path, value=executionStateString, makepath=True)
      return True
    except NoNodeError:
      raise_(StateException("NoNodeError while creating execution state",
                            StateException.EX_TYPE_NO_NODE_ERROR), sys.exc_info()[2])
    except NodeExistsError:
      raise_(StateException("NodeExistsError while creating execution state",
                            StateException.EX_TYPE_NODE_EXISTS_ERROR), sys.exc_info()[2])
    except ZookeeperError:
      raise_(StateException("Zookeeper while creating execution state",
                            StateException.EX_TYPE_ZOOKEEPER_ERROR), sys.exc_info()[2])
    except Exception:
      # Just re raise the exception.
      raise