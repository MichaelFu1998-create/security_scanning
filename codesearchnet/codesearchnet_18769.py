def add_all_filters(pelican):
    """Add (register) all filters to Pelican."""
    pelican.env.filters.update({'datetime': filters.datetime})
    pelican.env.filters.update({'article_date': filters.article_date})
    pelican.env.filters.update({'breaking_spaces': filters.breaking_spaces})
    pelican.env.filters.update({'titlecase': filters.titlecase})