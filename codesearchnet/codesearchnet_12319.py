def send_email(sender,
               subject,
               content,
               email_recipient_list,
               email_address_list,
               email_user=None,
               email_pass=None,
               email_server=None):
    '''This sends an email to addresses, informing them about events.

    The email account settings are retrieved from the settings file as described
    above.

    Parameters
    ----------

    sender : str
        The name of the sender to use in the email header.

    subject : str
        Subject of the email.

    content : str
        Content of the email.

    email_recipient list : list of str
        This is a list of email recipient names of the form:
        `['Example Person 1', 'Example Person 1', ...]`

    email_recipient list : list of str
        This is a list of email recipient addresses of the form:
        `['example1@example.com', 'example2@example.org', ...]`

    email_user : str
        The username of the email server account that will send the emails. If
        this is None, the value of EMAIL_USER from the
        ~/.astrobase/.emailsettings file will be used. If that is None as well,
        this function won't work.

    email_pass : str
        The password of the email server account that will send the emails. If
        this is None, the value of EMAIL_PASS from the
        ~/.astrobase/.emailsettings file will be used. If that is None as well,
        this function won't work.

    email_server : str
        The address of the email server that will send the emails. If this is
        None, the value of EMAIL_USER from the ~/.astrobase/.emailsettings file
        will be used. If that is None as well, this function won't work.

    Returns
    -------

    bool
        True if email sending succeeded. False if email sending failed.

    '''

    if not email_user:
        email_user = EMAIL_USER

    if not email_pass:
        email_pass = EMAIL_PASSWORD

    if not email_server:
        email_server = EMAIL_SERVER

    if not email_server and email_user and email_pass:
        raise ValueError("no email server address and "
                         "credentials available, can't continue")


    msg_text = EMAIL_TEMPLATE.format(
        sender=sender,
        hostname=socket.gethostname(),
        activity_time='%sZ' % datetime.utcnow().isoformat(),
        activity_report=content
    )

    email_sender = '%s <%s>' % (sender, EMAIL_USER)


    # put together the recipient and email lists
    email_recipients = [('%s <%s>' % (x,y))
                        for (x,y) in zip(email_recipient_list,
                                         email_address_list)]

    # put together the rest of the message
    email_msg = MIMEText(msg_text)
    email_msg['From'] = email_sender
    email_msg['To'] = ', '.join(email_recipients)
    email_msg['Message-Id'] = make_msgid()
    email_msg['Subject'] = '[%s on %s] %s' % (
        sender,
        socket.gethostname(),
        subject
    )
    email_msg['Date'] = formatdate(time.time())

    # start the email process

    try:
        server = smtplib.SMTP(EMAIL_SERVER, 587)
        server_ehlo_response = server.ehlo()

        if server.has_extn('STARTTLS'):

            try:

                tls_start_response = server.starttls()
                tls_ehlo_response = server.ehlo()

                login_response = server.login(EMAIL_USER, EMAIL_PASSWORD)

                send_response = (
                    server.sendmail(email_sender,
                                    email_address_list,
                                    email_msg.as_string())
                )

            except Exception as e:

                print('script email sending failed with error: %s'
                      % e)
                send_response = None

            if send_response is not None:

                print('script email sent successfully')
                quit_response = server.quit()
                return True

            else:

                quit_response = server.quit()
                return False

        else:

            print('email server does not support STARTTLS,'
                  ' bailing out...')
            quit_response = server.quit()
            return False

    except Exception as e:
        print('sending email failed with error: %s' % e)
        returnval = False


    quit_response = server.quit()
    return returnval