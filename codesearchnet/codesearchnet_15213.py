def sendMultiPart(smtp, gpg_context, sender, recipients, subject, text, attachments):
    """ a helper method that composes and sends an email with attachments
    requires a pre-configured smtplib.SMTP instance"""
    sent = 0
    for to in recipients:
        if not to.startswith('<'):
            uid = '<%s>' % to
        else:
            uid = to

        if not checkRecipient(gpg_context, uid):
            continue

        msg = MIMEMultipart()

        msg['From'] = sender
        msg['To'] = to
        msg['Subject'] = subject
        msg["Date"] = formatdate(localtime=True)
        msg.preamble = u'This is an email in encrypted multipart format.'

        attach = MIMEText(str(gpg_context.encrypt(text.encode('utf-8'), uid, always_trust=True)))
        attach.set_charset('UTF-8')
        msg.attach(attach)

        for attachment in attachments:
            with open(attachment, 'rb') as fp:
                attach = MIMEBase('application', 'octet-stream')
                attach.set_payload(str(gpg_context.encrypt_file(fp, uid, always_trust=True)))
            attach.add_header('Content-Disposition', 'attachment', filename=basename('%s.pgp' % attachment))
            msg.attach(attach)

        # TODO: need to catch exception?
        # yes :-) we need to adjust the status accordingly (>500 so it will be destroyed)
        smtp.begin()
        smtp.sendmail(sender, to, msg.as_string())
        smtp.quit()
        sent += 1

    return sent