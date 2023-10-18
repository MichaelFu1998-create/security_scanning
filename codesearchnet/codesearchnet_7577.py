def generate_dir_rst(src_dir, target_dir, gallery_conf, seen_backrefs):
    """Generate the gallery reStructuredText for an example directory"""
    if not os.path.exists(os.path.join(src_dir, 'README.txt')):
        print(80 * '_')
        print('Example directory %s does not have a README.txt file' %
              src_dir)
        print('Skipping this directory')
        print(80 * '_')
        return ""  # because string is an expected return type

    fhindex = open(os.path.join(src_dir, 'README.txt')).read()
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    sorted_listdir = [fname for fname in sorted(os.listdir(src_dir))
                      if fname.endswith('.py')]
    entries_text = []
    for fname in sorted_listdir:
        amount_of_code = generate_file_rst(fname, target_dir, src_dir,
                                           gallery_conf)
        new_fname = os.path.join(src_dir, fname)
        intro = extract_intro(new_fname)
        write_backreferences(seen_backrefs, gallery_conf,
                             target_dir, fname, intro)
        this_entry = _thumbnail_div(target_dir, fname, intro) + """

.. toctree::
   :hidden:

   /%s/%s\n""" % (target_dir, fname[:-3])
        entries_text.append((amount_of_code, this_entry))

    # sort to have the smallest entries in the beginning
    entries_text.sort()

    for _, entry_text in entries_text:
        fhindex += entry_text

    # clear at the end of the section
    fhindex += """.. raw:: html\n
    <div style='clear:both'></div>\n\n"""

    return fhindex