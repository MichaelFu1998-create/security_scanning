def delete_topology(self, topologyName):
    """ delete topology """
    path = self.get_topology_path(topologyName)
    LOG.info("Removing topology: {0} from path: {1}".format(
        topologyName, path))
    try:
      self.client.delete(path)
      return True
    except NoNodeError:
      raise_(StateException("NoNodeError while deteling topology",
                            StateException.EX_TYPE_NO_NODE_ERROR), sys.exc_info()[2])
    except NotEmptyError:
      raise_(StateException("NotEmptyError while deleting topology",
                            StateException.EX_TYPE_NOT_EMPTY_ERROR), sys.exc_info()[2])
    except ZookeeperError:
      raise_(StateException("Zookeeper while deleting topology",
                            StateException.EX_TYPE_ZOOKEEPER_ERROR), sys.exc_info()[2])
    except Exception:
      # Just re raise the exception.
      raise