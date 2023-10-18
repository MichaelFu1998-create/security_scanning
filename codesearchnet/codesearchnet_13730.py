def webhook_handler(*event_types):
	"""
	Decorator that registers a function as a webhook handler.

	Usage examples:

	>>> # Hook a single event
	>>> @webhook_handler("payment.sale.completed")
	>>> def on_payment_received(event):
	>>>     payment = event.get_resource()
	>>>     print("Received payment:", payment)

	>>> # Multiple events supported
	>>> @webhook_handler("billing.subscription.suspended", "billing.subscription.cancelled")
	>>> def on_subscription_stop(event):
	>>>     subscription = event.get_resource()
	>>>     print("Stopping subscription:", subscription)

	>>> # Using a wildcard works as well
	>>> @webhook_handler("billing.subscription.*")
	>>> def on_subscription_update(event):
	>>>     subscription = event.get_resource()
	>>>     print("Updated subscription:", subscription)
	"""

	# First expand all wildcards and verify the event types are valid
	event_types_to_register = set()
	for event_type in event_types:
		# Always convert to lowercase
		event_type = event_type.lower()
		if "*" in event_type:
			# expand it
			for t in WEBHOOK_EVENT_TYPES:
				if fnmatch(t, event_type):
					event_types_to_register.add(t)
		elif event_type not in WEBHOOK_EVENT_TYPES:
			raise ValueError("Unknown webhook event: %r" % (event_type))
		else:
			event_types_to_register.add(event_type)

	# Now register them
	def decorator(func):
		for event_type in event_types_to_register:
			WEBHOOK_SIGNALS[event_type].connect(func)
		return func

	return decorator