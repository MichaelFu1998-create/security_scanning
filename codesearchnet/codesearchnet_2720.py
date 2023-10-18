def template_uploader_yaml(cl_args, masters):
  '''
  Tempate uploader.yaml
  '''
  single_master = masters[0]
  uploader_config_template = "%s/standalone/templates/uploader.template.yaml" \
                             % cl_args["config_path"]
  uploader_config_actual = "%s/standalone/uploader.yaml" % cl_args["config_path"]

  template_file(uploader_config_template, uploader_config_actual,
                {"<http_uploader_uri>": "http://%s:9000/api/v1/file/upload" % single_master})