def get_user_details(user_id):
    """Get information about number of changesets, blocks and mapping days of a
    user, using both the OSM API and the Mapbox comments APIself.
    """
    reasons = []
    try:
        url = OSM_USERS_API.format(user_id=requests.compat.quote(user_id))
        user_request = requests.get(url)
        if user_request.status_code == 200:
            user_data = user_request.content
            xml_data = ET.fromstring(user_data).getchildren()[0].getchildren()
            changesets = [i for i in xml_data if i.tag == 'changesets'][0]
            blocks = [i for i in xml_data if i.tag == 'blocks'][0]
            if int(changesets.get('count')) <= 5:
                reasons.append('New mapper')
            elif int(changesets.get('count')) <= 30:
                url = MAPBOX_USERS_API.format(
                    user_id=requests.compat.quote(user_id)
                    )
                user_request = requests.get(url)
                if user_request.status_code == 200:
                    mapping_days = int(
                        user_request.json().get('extra').get('mapping_days')
                        )
                    if mapping_days <= 5:
                        reasons.append('New mapper')
            if int(blocks.getchildren()[0].get('count')) > 1:
                reasons.append('User has multiple blocks')
    except Exception as e:
        message = 'Could not verify user of the changeset: {}, {}'
        print(message.format(user_id, str(e)))
    return reasons