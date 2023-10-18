def sklearn2pmml(pipeline, pmml, user_classpath = [], with_repr = False, debug = False, java_encoding = "UTF-8"):
	"""Converts a fitted Scikit-Learn pipeline to PMML.

	Parameters:
	----------
	pipeline: PMMLPipeline
		The pipeline.

	pmml: string
		The path to where the PMML document should be stored.

	user_classpath: list of strings, optional
		The paths to JAR files that provide custom Transformer, Selector and/or Estimator converter classes.
		The JPMML-SkLearn classpath is constructed by appending user JAR files to package JAR files.

	with_repr: boolean, optional
		If true, insert the string representation of pipeline into the PMML document.

	debug: boolean, optional
		If true, print information about the conversion process.

	java_encoding: string, optional
		The character encoding to use for decoding Java output and error byte streams.

	"""
	if debug:
		java_version = _java_version(java_encoding)
		if java_version is None:
			java_version = ("java", "N/A")
		print("python: {0}".format(platform.python_version()))
		print("sklearn: {0}".format(sklearn.__version__))
		print("sklearn.externals.joblib: {0}".format(joblib.__version__))
		print("pandas: {0}".format(pandas.__version__))
		print("sklearn_pandas: {0}".format(sklearn_pandas.__version__))
		print("sklearn2pmml: {0}".format(__version__))
		print("{0}: {1}".format(java_version[0], java_version[1]))
	if not isinstance(pipeline, PMMLPipeline):
		raise TypeError("The pipeline object is not an instance of " + PMMLPipeline.__name__ + ". Use the 'sklearn2pmml.make_pmml_pipeline(obj)' utility function to translate a regular Scikit-Learn estimator or pipeline to a PMML pipeline")
	estimator = pipeline._final_estimator
	cmd = ["java", "-cp", os.pathsep.join(_classpath(user_classpath)), "org.jpmml.sklearn.Main"]
	dumps = []
	try:
		if with_repr:
			pipeline.repr_ = repr(pipeline)
		# if isinstance(estimator, H2OEstimator):
		if hasattr(estimator, "download_mojo"):
			estimator_mojo = estimator.download_mojo()
			dumps.append(estimator_mojo)
			estimator._mojo_path = estimator_mojo
		pipeline_pkl = _dump(pipeline, "pipeline")
		cmd.extend(["--pkl-pipeline-input", pipeline_pkl])
		dumps.append(pipeline_pkl)
		cmd.extend(["--pmml-output", pmml])
		if debug:
			print("Executing command:\n{0}".format(" ".join(cmd)))
		try:
			process = Popen(cmd, stdout = PIPE, stderr = PIPE, bufsize = 1)
		except OSError:
			raise RuntimeError("Java is not installed, or the Java executable is not on system path")
		output, error = process.communicate()
		retcode = process.poll()
		if debug or retcode:
			if(len(output) > 0):
				print("Standard output:\n{0}".format(_decode(output, java_encoding)))
			else:
				print("Standard output is empty")
			if(len(error) > 0):
				print("Standard error:\n{0}".format(_decode(error, java_encoding)))
			else:
				print("Standard error is empty")
		if retcode:
			raise RuntimeError("The JPMML-SkLearn conversion application has failed. The Java executable should have printed more information about the failure into its standard output and/or standard error streams")
	finally:
		if debug:
			print("Preserved joblib dump file(s): {0}".format(" ".join(dumps)))
		else:
			for dump in dumps:
				os.remove(dump)