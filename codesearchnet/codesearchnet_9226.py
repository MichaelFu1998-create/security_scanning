def compose_mbox(projects):
    """ Compose projects.json only for mbox, but using the mailing_lists lists

    change: 'https://dev.eclipse.org/mailman/listinfo/emft-dev'
    to: 'emfg-dev /home/bitergia/mboxes/emft-dev.mbox/emft-dev.mbox

    :param projects: projects.json
    :return: projects.json with mbox
    """
    mbox_archives = '/home/bitergia/mboxes'

    mailing_lists_projects = [project for project in projects if 'mailing_lists' in projects[project]]
    for mailing_lists in mailing_lists_projects:
        projects[mailing_lists]['mbox'] = []
        for mailing_list in projects[mailing_lists]['mailing_lists']:
            if 'listinfo' in mailing_list:
                name = mailing_list.split('listinfo/')[1]
            elif 'mailing-list' in mailing_list:
                name = mailing_list.split('mailing-list/')[1]
            else:
                name = mailing_list.split('@')[0]

            list_new = "%s %s/%s.mbox/%s.mbox" % (name, mbox_archives, name, name)
            projects[mailing_lists]['mbox'].append(list_new)

    return projects