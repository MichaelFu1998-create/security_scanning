def overview():
    """
        Provides an overview of the duplicate credentials.
    """
    search = Credential.search()
    search.aggs.bucket('password_count', 'terms', field='secret', order={'_count': 'desc'}, size=20)\
        .metric('username_count', 'cardinality', field='username') \
        .metric('host_count', 'cardinality', field='host_ip') \
        .metric('top_hits', 'top_hits', docvalue_fields=['username'], size=100)
    response = search.execute()
    print_line("{0:65} {1:5} {2:5} {3:5} {4}".format("Secret", "Count", "Hosts", "Users", "Usernames"))
    print_line("-"*100)
    for entry in response.aggregations.password_count.buckets:
        usernames = []
        for creds in entry.top_hits:
            usernames.append(creds.username[0])
        usernames = list(set(usernames))
        print_line("{0:65} {1:5} {2:5} {3:5} {4}".format(entry.key, entry.doc_count, entry.host_count.value, entry.username_count.value, usernames))