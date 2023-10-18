def load_py_instance(self, is_spout):
    """Loads user defined component (spout/bolt)"""
    try:
      if is_spout:
        spout_proto = self.pplan_helper.get_my_spout()
        py_classpath = spout_proto.comp.class_name
        self.logger.info("Loading Spout from: %s", py_classpath)
      else:
        bolt_proto = self.pplan_helper.get_my_bolt()
        py_classpath = bolt_proto.comp.class_name
        self.logger.info("Loading Bolt from: %s", py_classpath)

      pex_loader.load_pex(self.pplan_helper.topology_pex_abs_path)
      spbl_class = pex_loader.import_and_get_class(self.pplan_helper.topology_pex_abs_path,
                                                   py_classpath)
    except Exception as e:
      spbl = "spout" if is_spout else "bolt"
      self.logger.error(traceback.format_exc())
      raise RuntimeError("Error when loading a %s from pex: %s" % (spbl, str(e)))
    return spbl_class