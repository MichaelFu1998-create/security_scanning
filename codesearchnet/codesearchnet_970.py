def _generateMetricSpecString(inferenceElement, metric,
                              params=None, field=None,
                              returnLabel=False):
  """ Generates the string representation of a MetricSpec object, and returns
  the metric key associated with the metric.


  Parameters:
  -----------------------------------------------------------------------
  inferenceElement:
    An InferenceElement value that indicates which part of the inference this
    metric is computed on

  metric:
    The type of the metric being computed (e.g. aae, avg_error)

  params:
    A dictionary of parameters for the metric. The keys are the parameter names
    and the values should be the parameter values (e.g. window=200)

  field:
    The name of the field for which this metric is being computed

  returnLabel:
    If True, returns the label of the MetricSpec that was generated
  """

  metricSpecArgs = dict(metric=metric,
                        field=field,
                        params=params,
                        inferenceElement=inferenceElement)

  metricSpecAsString = "MetricSpec(%s)" % \
    ', '.join(['%s=%r' % (item[0],item[1])
              for item in metricSpecArgs.iteritems()])

  if not returnLabel:
    return metricSpecAsString

  spec = MetricSpec(**metricSpecArgs)
  metricLabel = spec.getLabel()
  return metricSpecAsString, metricLabel