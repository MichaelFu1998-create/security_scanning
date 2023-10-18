def search_engine(query, top=5, service="google", license=None,
                  cache=os.path.join(DEFAULT_CACHE, "google")):
    """
    Return a color aggregate from colors and ranges parsed from the web.
    T. De Smedt, http://nodebox.net/code/index.php/Prism
    """
    # Check if we have cached information first.
    try:
        a = theme(query, cache=cache)
        return a
    except:
        pass

    if service == "google":
        from web import google
        search_engine = google
    if service == "yahoo":
        from web import yahoo
        search_engine = yahoo
        if license:
            yahoo.license_key = license

    # Sort all the primary hues (plus black and white) for q.
    sorted_colors = search_engine.sort(
        [h for h in primary_hues] + ["black", "white"],
        context=query, strict=True, cached=True
    )

    # Sort all the shades (bright, hard, ...) for q.
    sorted_shades = search_engine.sort(
        [str(s) for s in shades],
        context=query, strict=True, cached=True
    )

    # Reforms '"black death"' to 'black'.
    f = lambda x: x.strip("\"").split()[0]

    # Take the top most relevant hues.
    n2 = sum([w for h, w in sorted_colors[:top]])
    sorted_colors = [(color(f(h)), w / n2) for h, w in sorted_colors[:top]]

    # Take the three most relevant shades.
    n2 = sum([w for s, w in sorted_shades[:3]])
    sorted_shades = [(shade(f(s)), w / n2) for s, w in sorted_shades[:3]]

    a = theme(cache=cache)
    a.name = query
    for clr, w1 in sorted_colors:
        for rng, w2 in sorted_shades:
            a.add_range(rng, clr, w1 * w2)

    a._save()
    return a