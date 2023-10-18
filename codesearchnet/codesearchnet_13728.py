def activate(self):
		"""
		Activate an plan in a CREATED state.
		"""
		obj = self.find_paypal_object()
		if obj.state == enums.BillingPlanState.CREATED:
			success = obj.activate()
			if not success:
				raise PaypalApiError("Failed to activate plan: %r" % (obj.error))
		# Resync the updated data to the database
		self.get_or_update_from_api_data(obj, always_sync=True)
		return obj