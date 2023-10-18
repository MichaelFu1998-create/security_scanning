def filter(self, **kwargs):
		'''
			filter - Add filters based on INDEXED_FIELDS having or not having a value.
			  Note, no objects are actually fetched until .all() is called

				Use the field name [ model.objects.filter(some_field='value')] to filter on items containing that value.
				Use the field name suffxed with '__ne' for a negation filter [ model.objects.filter(some_field__ne='value') ]

			Example:
				query = Model.objects.filter(field1='value', field2='othervalue')

				objs1 = query.filter(something__ne='value').all()
				objs2 = query.filter(something__ne=7).all()


			@returns - A copy of this object, with the additional filters. If you want to work inline on this object instead, use the filterInline method.
		'''
		selfCopy = self.__copy__()
		return IndexedRedisQuery._filter(selfCopy, **kwargs)