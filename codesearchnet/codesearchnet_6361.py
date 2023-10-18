def _sbase_annotations(sbase, annotation):
    """Set SBase annotations based on cobra annotations.

    Parameters
    ----------
    sbase : libsbml.SBase
        SBML object to annotate
    annotation : cobra annotation structure
        cobra object with annotation information

    FIXME: annotation format must be updated
        (https://github.com/opencobra/cobrapy/issues/684)
    """

    if not annotation or len(annotation) == 0:
        return

    # standardize annotations
    annotation_data = deepcopy(annotation)

    for key, value in annotation_data.items():
        # handling of non-string annotations (e.g. integers)
        if isinstance(value, (float, int)):
            value = str(value)
        if isinstance(value, string_types):
            annotation_data[key] = [("is", value)]

    for key, value in annotation_data.items():
        for idx, item in enumerate(value):
            if isinstance(item, string_types):
                value[idx] = ("is", item)

    # set metaId
    meta_id = "meta_{}".format(sbase.getId())
    sbase.setMetaId(meta_id)

    # rdf_items = []
    for provider, data in iteritems(annotation_data):

        # set SBOTerm
        if provider in ["SBO", "sbo"]:
            if provider == "SBO":
                LOGGER.warning("'SBO' provider is deprecated, "
                               "use 'sbo' provider instead")
            sbo_term = data[0][1]
            _check(sbase.setSBOTerm(sbo_term),
                   "Setting SBOTerm: {}".format(sbo_term))

            # FIXME: sbo should also be written as CVTerm
            continue

        for item in data:
            qualifier_str, entity = item[0], item[1]
            qualifier = QUALIFIER_TYPES.get(qualifier_str, None)
            if qualifier is None:
                qualifier = libsbml.BQB_IS
                LOGGER.error("Qualifier type is not supported on "
                             "annotation: '{}'".format(qualifier_str))

            qualifier_type = libsbml.BIOLOGICAL_QUALIFIER
            if qualifier_str.startswith("bqm_"):
                qualifier_type = libsbml.MODEL_QUALIFIER

            cv = libsbml.CVTerm()  # type: libsbml.CVTerm
            cv.setQualifierType(qualifier_type)
            if qualifier_type == libsbml.BIOLOGICAL_QUALIFIER:
                cv.setBiologicalQualifierType(qualifier)
            elif qualifier_type == libsbml.MODEL_QUALIFIER:
                cv.setModelQualifierType(qualifier)
            else:
                raise CobraSBMLError('Unsupported qualifier: '
                                     '%s' % qualifier)
            resource = "%s/%s/%s" % (URL_IDENTIFIERS_PREFIX, provider, entity)
            cv.addResource(resource)
            _check(sbase.addCVTerm(cv),
                   "Setting cvterm: {}, resource: {}".format(cv, resource))