def _generateMetricsSubstitutions(options, tokenReplacements):
  """Generate the token substitution for metrics related fields.
  This includes:
    \$METRICS
    \$LOGGED_METRICS
    \$PERM_OPTIMIZE_SETTING
  """
  # -----------------------------------------------------------------------
  #
  options['loggedMetrics'] = [".*"]

  # -----------------------------------------------------------------------
  # Generate the required metrics
  metricList, optimizeMetricLabel = _generateMetricSpecs(options)

  metricListString = ",\n".join(metricList)
  metricListString = _indentLines(metricListString, 2, indentFirstLine=False)
  permOptimizeSettingStr = 'minimize = "%s"' % optimizeMetricLabel
  # -----------------------------------------------------------------------
  # Specify which metrics should be logged
  loggedMetricsListAsStr = "[%s]" % (", ".join(["'%s'"% ptrn
                                              for ptrn in options['loggedMetrics']]))


  tokenReplacements['\$LOGGED_METRICS'] \
                                        = loggedMetricsListAsStr

  tokenReplacements['\$METRICS'] = metricListString

  tokenReplacements['\$PERM_OPTIMIZE_SETTING'] \
                                        = permOptimizeSettingStr