def create_topology(self, topologyName, topology):
    """ crate topology """
    if not topology or not topology.IsInitialized():
      raise_(StateException("Topology protobuf not init properly",
                            StateException.EX_TYPE_PROTOBUF_ERROR), sys.exc_info()[2])

    path = self.get_topology_path(topologyName)
    LOG.info("Adding topology: {0} to path: {1}".format(
        topologyName, path))
    topologyString = topology.SerializeToString()
    try:
      self.client.create(path, value=topologyString, makepath=True)
      return True
    except NoNodeError:
      raise_(StateException("NoNodeError while creating topology",
                            StateException.EX_TYPE_NO_NODE_ERROR), sys.exc_info()[2])
    except NodeExistsError:
      raise_(StateException("NodeExistsError while creating topology",
                            StateException.EX_TYPE_NODE_EXISTS_ERROR), sys.exc_info()[2])
    except ZookeeperError:
      raise_(StateException("Zookeeper while creating topology",
                            StateException.EX_TYPE_ZOOKEEPER_ERROR), sys.exc_info()[2])
    except Exception:
      # Just re raise the exception.
      raise