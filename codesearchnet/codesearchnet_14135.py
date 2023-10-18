def examples_menu(root_dir=None, depth=0):
    """
    :return: xml for menu, [(bot_action, label), ...], [(menu_action, label), ...]
    """
    # pre 3.12 menus
    examples_dir = ide_utils.get_example_dir()
    if not examples_dir:
        return "", [], []

    root_dir = root_dir or examples_dir

    file_tmpl = '<menuitem name="{name}" action="{action}"/>'
    dir_tmpl = '<menu name="{name}" action="{action}">{menu}</menu>'

    file_actions = []
    submenu_actions = []

    xml = ""

    for fn in sorted(os.listdir(root_dir)):
        path = os.path.join(root_dir, fn)
        rel_path = path[len(examples_dir):]
        if os.path.isdir(path):
            action = 'ShoebotExampleMenu {0}'.format(rel_path)
            label = fn.capitalize()

            sm_xml, sm_file_actions, sm_menu_actions = examples_menu(os.path.join(root_dir, fn), depth+1)

            submenu_actions.extend(sm_menu_actions)
            file_actions.extend(sm_file_actions)
            submenu_actions.append((action, label))
            xml += dir_tmpl.format(name=fn, action=action, menu=sm_xml)
        elif os.path.splitext(path)[1] in ['.bot', '.py'] and not fn.startswith('_'):
            action = 'ShoebotExampleOpen {0}'.format(rel_path)
            label = ide_utils.make_readable_filename(fn)

            xml += file_tmpl.format(name=fn, action=action)
            file_actions.append((action, label))

    return xml, file_actions, submenu_actions