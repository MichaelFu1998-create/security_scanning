def extract_hook_names(ent):
    """Extract hook names from the given entity"""

    hnames = []
    for hook in ent["hooks"]["enter"] + ent["hooks"]["exit"]:
        hname = os.path.basename(hook["fpath_orig"])
        hname = os.path.splitext(hname)[0]
        hname = hname.strip()
        hname = hname.replace("_enter", "")
        hname = hname.replace("_exit", "")
        if hname in hnames:
            continue

        hnames.append(hname)

    hnames.sort()

    return hnames