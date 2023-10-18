def make_pmml_pipeline(obj, active_fields = None, target_fields = None):
	"""Translates a regular Scikit-Learn estimator or pipeline to a PMML pipeline.

	Parameters:
	----------
	obj: BaseEstimator
		The object.

	active_fields: list of strings, optional
		Feature names. If missing, "x1", "x2", .., "xn" are assumed.

	target_fields: list of strings, optional
		Label name(s). If missing, "y" is assumed.

	"""
	steps = _filter_steps(_get_steps(obj))
	pipeline = PMMLPipeline(steps)
	if active_fields is not None:
		pipeline.active_fields = numpy.asarray(active_fields)
	if target_fields is not None:
		pipeline.target_fields = numpy.asarray(target_fields)
	return pipeline