def create_pplan(self, topologyName, pplan):
    """ create physical plan """
    if not pplan or not pplan.IsInitialized():
      raise_(StateException("Physical Plan protobuf not init properly",
                            StateException.EX_TYPE_PROTOBUF_ERROR), sys.exc_info()[2])

    path = self.get_pplan_path(topologyName)
    LOG.info("Adding topology: {0} to path: {1}".format(
        topologyName, path))
    pplanString = pplan.SerializeToString()
    try:
      self.client.create(path, value=pplanString, makepath=True)
      return True
    except NoNodeError:
      raise_(StateException("NoNodeError while creating pplan",
                            StateException.EX_TYPE_NO_NODE_ERROR), sys.exc_info()[2])
    except NodeExistsError:
      raise_(StateException("NodeExistsError while creating pplan",
                            StateException.EX_TYPE_NODE_EXISTS_ERROR), sys.exc_info()[2])
    except ZookeeperError:
      raise_(StateException("Zookeeper while creating pplan",
                            StateException.EX_TYPE_ZOOKEEPER_ERROR), sys.exc_info()[2])
    except Exception:
      # Just re raise the exception.
      raise