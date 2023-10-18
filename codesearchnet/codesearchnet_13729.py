def execute(self):
		"""
		Execute the PreparedBillingAgreement by creating and executing a
		matching BillingAgreement.
		"""
		# Save the execution time first.
		# If execute() fails, executed_at will be set, with no executed_agreement set.
		self.executed_at = now()
		self.save()

		with transaction.atomic():
			ret = BillingAgreement.execute(self.id)
			ret.user = self.user
			ret.save()
			self.executed_agreement = ret
			self.save()

		return ret