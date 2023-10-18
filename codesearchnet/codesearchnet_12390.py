def find_and_patch_entry(soup, entry):
    """
    Modify soup so Dash.app can generate TOCs on the fly.
    """
    link = soup.find("a", {"class": "headerlink"}, href="#" + entry.anchor)
    tag = soup.new_tag("a")
    tag["name"] = APPLE_REF_TEMPLATE.format(entry.type, entry.name)
    if link:
        link.parent.insert(0, tag)
        return True
    elif entry.anchor.startswith("module-"):
        soup.h1.parent.insert(0, tag)
        return True
    else:
        return False