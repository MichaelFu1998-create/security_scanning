def upload(ctx, browse=False, target=None, release='latest'):
    """Upload a ZIP of built docs (by default to PyPI, else a WebDAV URL)."""
    cfg = config.load()
    uploader = DocsUploader(ctx, cfg, target)

    html_dir = os.path.join(ctx.rituals.docs.sources, ctx.rituals.docs.build)
    if not os.path.isdir(html_dir):
        notify.failure("No HTML docs dir found at '{}'!".format(html_dir))

    url = uploader.upload(html_dir, release)
    notify.info("Uploaded docs to '{url}'!".format(url=url or 'N/A'))
    if url and browse:  # Open in browser?
        webbrowser.open_new_tab(url)