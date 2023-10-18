def long_description():
    """Generate .rst document for PyPi."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--doc', dest="doc",
            action="store_true", default=False)
    args, sys.argv = parser.parse_known_args(sys.argv)
    if args.doc:
        import doc2md, pypandoc
        md = doc2md.doc2md(doc2md.__doc__, "doc2md", toc=False)
        long_description = pypandoc.convert(md, 'rst', format='md')
    else:
        return None