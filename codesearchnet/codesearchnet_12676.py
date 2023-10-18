def main(sample=False,
         dry_run=True,
         limit=1,
         no_limit=False,
         database_filename=DATABASE_FILENAME_DEFAULT,
         template_filename=TEMPLATE_FILENAME_DEFAULT,
         config_filename=CONFIG_FILENAME_DEFAULT):
    """Python API for mailmerge.

    mailmerge 0.1 by Andrew DeOrio <awdeorio@umich.edu>.

    A simple, command line mail merge tool.

    Render an email template for each line in a CSV database.
    """
    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches
    # pylint: disable=too-many-statements
    # NOTE: this function needs a refactor, then remove ^^^
    # Create a sample email template and database if there isn't one already
    if sample:
        create_sample_input_files(
            template_filename,
            database_filename,
            config_filename,
        )
        sys.exit(0)
    if not os.path.exists(template_filename):
        print("Error: can't find template email " + template_filename)
        print("Create a sample (--sample) or specify a file (--template)")
        sys.exit(1)
    if not os.path.exists(database_filename):
        print("Error: can't find database_filename " + database_filename)
        print("Create a sample (--sample) or specify a file (--database)")
        sys.exit(1)

    try:
        # Read template
        with io.open(template_filename, "r") as template_file:
            content = template_file.read() + u"\n"
            template = jinja2.Template(content)

        # Read CSV file database
        database = []
        with io.open(database_filename, "r") as database_file:
            reader = csv.DictReader(database_file)
            for row in reader:
                database.append(row)

        # Each row corresponds to one email message
        for i, row in enumerate(database):
            if not no_limit and i >= limit:
                break

            # Fill in template fields using fields from row of CSV file
            raw_message = template.render(**row)

            # Parse message headers and detect encoding
            (message, sender, recipients) = parsemail(raw_message)
            # Convert message from markdown to HTML if requested
            if message['Content-Type'].startswith("text/markdown"):
                message = convert_markdown(message)

            print(">>> message {}".format(i))
            print(message.as_string())

            # Add attachments if any
            (message, num_attachments) = addattachments(message,
                                                        template_filename)

            # Send message
            if dry_run:
                print(">>> sent message {} DRY RUN".format(i))
            else:
                # Send message
                try:
                    sendmail(message, sender, recipients, config_filename)
                except smtplib.SMTPException as err:
                    print(">>> failed to send message {}".format(i))
                    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(
                        datetime.datetime.now()
                    )
                    print(timestamp, i, err, sep=' ', file=sys.stderr)
                else:
                    print(">>> sent message {}".format(i))

        # Hints for user
        if num_attachments == 0:
            print(">>> No attachments were sent with the emails.")
        if not no_limit:
            print(">>> Limit was {} messages.  ".format(limit) +
                  "To remove the limit, use the --no-limit option.")
        if dry_run:
            print((">>> This was a dry run.  "
                   "To send messages, use the --no-dry-run option."))

    except jinja2.exceptions.TemplateError as err:
        print(">>> Error in Jinja2 template: {}".format(err))
        sys.exit(1)
    except csv.Error as err:
        print(">>> Error reading CSV file: {}".format(err))
        sys.exit(1)
    except smtplib.SMTPAuthenticationError as err:
        print(">>> Authentication error: {}".format(err))
        sys.exit(1)
    except configparser.Error as err:
        print(">>> Error reading config file {}: {}".format(
            config_filename, err))
        sys.exit(1)