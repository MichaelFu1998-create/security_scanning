def generate_simple_chemical_query(self, name=None, chemical_formula=None, property_name=None, property_value=None,
                                       property_min=None, property_max=None, property_units=None, reference_doi=None,
                                       include_datasets=[], exclude_datasets=[], from_index=None, size=None):
        """
        This method generates a :class:`PifSystemReturningQuery` object using the
        supplied arguments. All arguments that accept lists have logical OR's on the queries that they generate.
        This means that, for example, simple_chemical_search(name=['A', 'B']) will match records that have name
        equal to 'A' or 'B'.

        Results will be pulled into the extracted field of the :class:`PifSearchHit` objects that are returned. The
        name will appear under the key "name", chemical formula under "chemical_formula", property name under
        "property_name", value of the property under "property_value", units of the property under "property_units",
        and reference DOI under "reference_doi".

        This method is only meant for execution of very simple queries. More complex queries must use the search method
        that accepts a :class:`PifSystemReturningQuery` object.

        :param name: One or more strings with the names of the chemical system to match.
        :type name: str or list of str
        :param chemical_formula:  One or more strings with the chemical formulas to match.
        :type chemical_formula: str or list of str
        :param property_name: One or more strings with the names of the property to match.
        :type property_name: str or list of str
        :param property_value: One or more strings or numbers with the exact values to match.
        :type property_value: str or int or float or list of str or int or float
        :param property_min: A single string or number with the minimum value to match.
        :type property_min: str or int or float
        :param property_max: A single string or number with the maximum value to match.
        :type property_max: str or int or float
        :param property_units: One or more strings with the property units to match.
        :type property_units: str or list of str
        :param reference_doi: One or more strings with the DOI to match.
        :type reference_doin: str or list of str
        :param include_datasets: One or more integers with dataset IDs to match.
        :type include_datasets: int or list of int
        :param exclude_datasets: One or more integers with dataset IDs that must not match.
        :type exclude_datasets: int or list of int
        :param from_index: Index of the first record to match.
        :type from_index: int
        :param size: Total number of records to return.
        :type size: int
        :return: A query to to be submitted with the pif_search method
        :rtype: :class:`PifSystemReturningQuery`
        """
        pif_system_query = PifSystemQuery()
        pif_system_query.names = FieldQuery(
            extract_as='name',
            filter=[Filter(equal=i) for i in self._get_list(name)])
        pif_system_query.chemical_formula = ChemicalFieldQuery(
            extract_as='chemical_formula',
            filter=[ChemicalFilter(equal=i) for i in self._get_list(chemical_formula)])
        pif_system_query.references = ReferenceQuery(doi=FieldQuery(
            extract_as='reference_doi',
            filter=[Filter(equal=i) for i in self._get_list(reference_doi)]))

        # Generate the parts of the property query
        property_name_query = FieldQuery(
            extract_as='property_name',
            filter=[Filter(equal=i) for i in self._get_list(property_name)])
        property_units_query = FieldQuery(
            extract_as='property_units',
            filter=[Filter(equal=i) for i in self._get_list(property_units)])
        property_value_query = FieldQuery(
            extract_as='property_value',
            filter=[])
        for i in self._get_list(property_value):
            property_value_query.filter.append(Filter(equal=i))
        if property_min is not None or property_max is not None:
            property_value_query.filter.append(Filter(min=property_min, max=property_max))

        # Generate the full property query
        pif_system_query.properties = PropertyQuery(
            name=property_name_query,
            value=property_value_query,
            units=property_units_query)

        # Generate the dataset query
        dataset_query = list()
        if include_datasets:
            dataset_query.append(DatasetQuery(logic='MUST', id=[Filter(equal=i) for i in include_datasets]))
        if exclude_datasets:
            dataset_query.append(DatasetQuery(logic='MUST_NOT', id=[Filter(equal=i) for i in exclude_datasets]))

        # Run the query
        pif_system_returning_query = PifSystemReturningQuery(
            query=DataQuery(
                system=pif_system_query,
                dataset=dataset_query),
            from_index=from_index,
            size=size,
            score_relevance=True)

        return pif_system_returning_query