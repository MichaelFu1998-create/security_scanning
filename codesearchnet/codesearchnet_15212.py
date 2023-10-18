def setup_smtp_factory(**settings):
    """ expects a dictionary with 'mail.' keys to create an appropriate smtplib.SMTP instance"""
    return CustomSMTP(
        host=settings.get('mail.host', 'localhost'),
        port=int(settings.get('mail.port', 25)),
        user=settings.get('mail.user'),
        password=settings.get('mail.password'),
        timeout=float(settings.get('mail.timeout', 60)),
    )