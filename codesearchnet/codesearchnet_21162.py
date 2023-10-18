def validateModel(model):
		'''
			validateModel - Class method that validates a given model is implemented correctly. Will only be validated once, on first model instantiation.

			@param model - Implicit of own class

			@return - True

			@raises - InvalidModelException if there is a problem with the model, and the message contains relevant information.
		'''
		if model == IndexedRedisModel:
			import re
			if re.match('.*pydoc(|[\d]|[\d][\.][\d])([\.]py(|[co])){0,1}$', sys.argv[0]):
				return
			raise ValueError('Cannot use IndexedRedisModel directly. You must implement this class for your model.')

		global validatedModels
		keyName = model.KEY_NAME
		if not keyName:
			raise InvalidModelException('"%s" has no KEY_NAME defined.' %(str(model.__name__), ) )

		if model in validatedModels:
			return True

		failedValidationStr = '"%s" Failed Model Validation:' %(str(model.__name__), ) 

		# Convert items in model to set
		#model.FIELDS = set(model.FIELDS)

		
		fieldSet = set(model.FIELDS)
		indexedFieldSet = set(model.INDEXED_FIELDS)

		if not fieldSet:
			raise InvalidModelException('%s No fields defined. Please populate the FIELDS array with a list of field names' %(failedValidationStr,))


		if hasattr(model, 'BASE64_FIELDS'):
			raise InvalidModelException('BASE64_FIELDS is no longer supported since IndexedRedis 5.0.0 . Use IndexedRedis.fields.IRBase64Field in the FIELDS array for the same functionality.')

		if hasattr(model, 'BINARY_FIELDS'):
			raise InvalidModelException('BINARY_FIELDS is no longer supported since IndexedRedis 5.0.0 . Use IndexedRedis.fields.IRBytesField in the FIELDS array for the same functionality, use IRBytesField for same functionality. Use IRField(valueType=bytes) for python-3 only support. Use IRRawField to perform no conversion at all.')

		newFields = []
		updatedFields = []
		mustUpdateFields = False

		foreignFields = []

		for thisField in fieldSet:
			if thisField == '_id':
				raise InvalidModelException('%s You cannot have a field named _id, it is reserved for the primary key.' %(failedValidationStr,))

			# XXX: Is this ascii requirement still needed since all is unicode now?
			try:
				codecs.ascii_encode(thisField)
			except UnicodeDecodeError as e:
				raise InvalidModelException('%s All field names must be ascii-encodable. "%s" was not. Error was: %s' %(failedValidationStr, to_unicode(thisField), str(e)))

			if issubclass(thisField.__class__, IRForeignLinkFieldBase):
				foreignFields.append(thisField)

			# If a classic string field, convert to IRClassicField
			if issubclass(thisField.__class__, IRField):
				newFields.append(thisField)
			else:
				mustUpdateFields = True
				newField = IRClassicField(thisField)
				newFields.append(newField)
				updatedFields.append(thisField)

				thisField = newField

			if str(thisField) == '':
				raise InvalidModelException('%s Field defined without a name, or name was an empty string. Type=%s  Field is:  %s' %(failedValidationStr, str(type(thisField)), repr(thisField)   ) )

			if thisField in indexedFieldSet and thisField.CAN_INDEX is False:
				raise InvalidModelException('%s Field Type %s - (%s) cannot be indexed.' %(failedValidationStr, str(thisField.__class__.__name__), repr(thisField)))

			if hasattr(IndexedRedisModel, thisField) is True:
				raise InvalidModelException('%s Field name %s is a reserved attribute on IndexedRedisModel.' %(failedValidationStr, str(thisField)))



		if mustUpdateFields is True:
			model.FIELDS = newFields
			deprecatedMessage('Model "%s" contains plain-string fields. These have been converted to IRClassicField objects to retain the same functionality. plain-string fields will be removed in a future version. The converted fields are: %s' %(model.__name__, repr(updatedFields)), 'UPDATED_FIELDS_' + model.__name__)

		model.FIELDS = KeyList(model.FIELDS)

		if bool(indexedFieldSet - fieldSet):
			raise InvalidModelException('%s All INDEXED_FIELDS must also be present in FIELDS. %s exist only in INDEXED_FIELDS' %(failedValidationStr, str(list(indexedFieldSet - fieldSet)), ) )

		model.foreignFields = foreignFields
		
		validatedModels.add(model)
		return True