def process_request(self, request):
        """Check if each request is allowed to access the current resource."""
        try:
            session = request.session
        except AttributeError:
            raise ImproperlyConfigured('django-lockdown requires the Django '
                                       'sessions framework')

        # Don't lock down if django-lockdown is disabled altogether.
        if settings.ENABLED is False:
            return None

        # Don't lock down if the client REMOTE_ADDR matched and is part of the
        # exception list.
        if self.remote_addr_exceptions:
            remote_addr_exceptions = self.remote_addr_exceptions
        else:
            remote_addr_exceptions = settings.REMOTE_ADDR_EXCEPTIONS

        if remote_addr_exceptions:
            # If forwarding proxies are used they must be listed as trusted
            trusted_proxies = self.trusted_proxies or settings.TRUSTED_PROXIES

            remote_addr = request.META.get('REMOTE_ADDR')
            if remote_addr in remote_addr_exceptions:
                return None
            if remote_addr in trusted_proxies:
                # If REMOTE_ADDR is a trusted proxy check x-forwarded-for
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    remote_addr = x_forwarded_for.split(',')[-1].strip()
                    if remote_addr in remote_addr_exceptions:
                        return None

        # Don't lock down if the URL matches an exception pattern.
        if self.url_exceptions:
            url_exceptions = compile_url_exceptions(self.url_exceptions)
        else:
            url_exceptions = compile_url_exceptions(settings.URL_EXCEPTIONS)
        for pattern in url_exceptions:
            if pattern.search(request.path):
                return None

        # Don't lock down if the URL resolves to a whitelisted view.
        try:
            resolved_path = resolve(request.path)
        except Resolver404:
            pass
        else:
            if resolved_path.func in settings.VIEW_EXCEPTIONS:
                return None

        # Don't lock down if outside of the lockdown dates.
        if self.until_date:
            until_date = self.until_date
        else:
            until_date = settings.UNTIL_DATE

        if self.after_date:
            after_date = self.after_date
        else:
            after_date = settings.AFTER_DATE

        if until_date or after_date:
            locked_date = False
            if until_date and datetime.datetime.now() < until_date:
                locked_date = True
            if after_date and datetime.datetime.now() > after_date:
                locked_date = True
            if not locked_date:
                return None

        form_data = request.POST if request.method == 'POST' else None
        if self.form:
            form_class = self.form
        else:
            form_class = get_lockdown_form(settings.FORM)
        form = form_class(data=form_data, **self.form_kwargs)

        authorized = False
        token = session.get(self.session_key)
        if hasattr(form, 'authenticate'):
            if form.authenticate(token):
                authorized = True
        elif token is True:
            authorized = True

        if authorized and self.logout_key and self.logout_key in request.GET:
            if self.session_key in session:
                del session[self.session_key]
            querystring = request.GET.copy()
            del querystring[self.logout_key]
            return self.redirect(request)

        # Don't lock down if the user is already authorized for previewing.
        if authorized:
            return None

        if form.is_valid():
            if hasattr(form, 'generate_token'):
                token = form.generate_token()
            else:
                token = True
            session[self.session_key] = token
            return self.redirect(request)

        page_data = {'until_date': until_date, 'after_date': after_date}
        if not hasattr(form, 'show_form') or form.show_form():
            page_data['form'] = form

        if self.extra_context:
            page_data.update(self.extra_context)

        return render(request, 'lockdown/form.html', page_data)