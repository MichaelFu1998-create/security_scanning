def pypinfo(
    ctx,
    project,
    fields,
    auth,
    run,
    json,
    indent,
    timeout,
    limit,
    days,
    start_date,
    end_date,
    where,
    order,
    all_installers,
    percent,
    markdown,
):
    """Valid fields are:\n
    project | version | file | pyversion | percent3 | percent2 | impl | impl-version |\n
    openssl | date | month | year | country | installer | installer-version |\n
    setuptools-version | system | system-release | distro | distro-version | cpu
    """
    if auth:
        set_credentials(auth)
        click.echo('Credentials location set to "{}".'.format(get_credentials()))
        return

    if project is None and not fields:
        click.echo(ctx.get_help())
        return

    parsed_fields = []
    for field in fields:
        parsed = FIELD_MAP.get(field)
        if parsed is None:
            raise ValueError('"{}" is an unsupported field.'.format(field))
        parsed_fields.append(parsed)

    order_name = order
    order = FIELD_MAP.get(order)
    if order:
        order_name = order.name
        parsed_fields.insert(0, order)

    built_query = build_query(
        project,
        parsed_fields,
        limit=limit,
        days=days,
        start_date=start_date,
        end_date=end_date,
        where=where,
        order=order_name,
        pip=not all_installers,
    )

    if run:
        client = create_client(get_credentials())
        query_job = client.query(built_query, job_config=create_config())
        query_rows = query_job.result(timeout=timeout // 1000)

        # Cached
        from_cache = not not query_job.cache_hit

        # Processed
        bytes_processed = query_job.total_bytes_processed or 0
        processed_amount, processed_unit = convert_units(bytes_processed)

        # Billed
        bytes_billed = query_job.total_bytes_billed or 0
        billed_amount, billed_unit = convert_units(bytes_billed)

        # Cost
        billing_tier = query_job.billing_tier or 1
        estimated_cost = Decimal(TIER_COST * billing_tier) / TB * Decimal(bytes_billed)
        estimated_cost = str(estimated_cost.quantize(TO_CENTS, rounding=ROUND_UP))

        rows = parse_query_result(query_job, query_rows)

        if percent:
            rows = add_percentages(rows, include_sign=not json)

        # Only for tables, and if more than the header row + a single data row
        if len(rows) > 2 and not json:
            rows = add_download_total(rows)

        if not json:
            click.echo('Served from cache: {}'.format(from_cache))
            click.echo('Data processed: {:.2f} {}'.format(processed_amount, processed_unit))
            click.echo('Data billed: {:.2f} {}'.format(billed_amount, billed_unit))
            click.echo('Estimated cost: ${}'.format(estimated_cost))

            click.echo()
            click.echo(tabulate(rows, markdown))
        else:
            query_info = {
                'cached': from_cache,
                'bytes_processed': bytes_processed,
                'bytes_billed': bytes_billed,
                'estimated_cost': estimated_cost,
            }
            click.echo(format_json(rows, query_info, indent))
    else:
        click.echo(built_query)