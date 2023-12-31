def contact(request):
    """Displays the contact form and sends the email"""
    form = ContactForm(request.POST or None)
    if form.is_valid():
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        sender = form.cleaned_data['sender']
        cc_myself = form.cleaned_data['cc_myself']

        recipients = settings.CONTACTFORM_RECIPIENTS
        if cc_myself:
            recipients.append(sender)

        send_mail(getattr(settings, "CONTACTFORM_SUBJECT_PREFIX", '') + subject, message, sender, recipients)

        return render(request, 'contactform/thanks.html')

    return render( request, 'contactform/contact.html', {'form': form})