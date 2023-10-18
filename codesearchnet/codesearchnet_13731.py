def from_request(cls, request, webhook_id=PAYPAL_WEBHOOK_ID):
		"""
		Create, validate and process a WebhookEventTrigger given a Django
		request object.

		The webhook_id parameter expects the ID of the Webhook that was
		triggered (defaults to settings.PAYPAL_WEBHOOK_ID). This is required
		for Webhook verification.

		The process is three-fold:
		1. Create a WebhookEventTrigger object from a Django request.
		2. Verify the WebhookEventTrigger as a Paypal webhook using the SDK.
		3. If valid, process it into a WebhookEvent object (and child resource).
		"""

		headers = fix_django_headers(request.META)
		assert headers
		try:
			body = request.body.decode(request.encoding or "utf-8")
		except Exception:
			body = "(error decoding body)"

		ip = request.META["REMOTE_ADDR"]
		obj = cls.objects.create(headers=headers, body=body, remote_ip=ip)

		try:
			obj.valid = obj.verify(PAYPAL_WEBHOOK_ID)
			if obj.valid:
				# Process the item (do not save it, it'll get saved below)
				obj.process(save=False)
		except Exception as e:
			max_length = WebhookEventTrigger._meta.get_field("exception").max_length
			obj.exception = str(e)[:max_length]
			obj.traceback = format_exc()
		finally:
			obj.save()

		return obj