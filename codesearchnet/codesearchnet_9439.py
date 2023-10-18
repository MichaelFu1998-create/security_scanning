def timeline(ctx, pager, limit, twtfile, sorting, timeout, porcelain, source, cache, force_update):
    """Retrieve your personal timeline."""
    if source:
        source_obj = ctx.obj["conf"].get_source_by_nick(source)
        if not source_obj:
            logger.debug("Not following {0}, trying as URL".format(source))
            source_obj = Source(source, source)
        sources = [source_obj]
    else:
        sources = ctx.obj["conf"].following

    tweets = []

    if cache:
        try:
            with Cache.discover(update_interval=ctx.obj["conf"].timeline_update_interval) as cache:
                force_update = force_update or not cache.is_valid
                if force_update:
                    tweets = get_remote_tweets(sources, limit, timeout, cache)
                else:
                    logger.debug("Multiple calls to 'timeline' within {0} seconds. Skipping update".format(
                        cache.update_interval))
                    # Behold, almighty list comprehensions! (I might have gone overboard here…)
                    tweets = list(chain.from_iterable([cache.get_tweets(source.url) for source in sources]))
        except OSError as e:
            logger.debug(e)
            tweets = get_remote_tweets(sources, limit, timeout)
    else:
        tweets = get_remote_tweets(sources, limit, timeout)

    if twtfile and not source:
        source = Source(ctx.obj["conf"].nick, ctx.obj["conf"].twturl, file=twtfile)
        tweets.extend(get_local_tweets(source, limit))

    if not tweets:
        return

    tweets = sort_and_truncate_tweets(tweets, sorting, limit)

    if pager:
        click.echo_via_pager(style_timeline(tweets, porcelain))
    else:
        click.echo(style_timeline(tweets, porcelain))