def _generate_automatic_headline(c):
    """The only field that maps closely to Open511 <headline>, a required field, is optional
    in TMDD. So we sometimes need to generate our own."""
    # Start with the event type, e.g. "Incident"
    headline = c.data['event_type'].replace('_', ' ').title()
    if c.data['roads']:
        # Add the road name
        headline += ' on ' + c.data['roads'][0]['name']
        direction = c.data['roads'][0].get('direction')
        if direction and direction not in ('BOTH', 'NONE'):
            headline += ' ' + direction
    return headline