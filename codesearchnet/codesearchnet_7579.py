def generate_file_rst(fname, target_dir, src_dir, gallery_conf):
    """ Generate the rst file for a given example.

        Returns the amout of code (in characters) of the corresponding
        files.
    """

    src_file = os.path.join(src_dir, fname)
    example_file = os.path.join(target_dir, fname)
    shutil.copyfile(src_file, example_file)

    image_dir = os.path.join(target_dir, 'images')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    base_image_name = os.path.splitext(fname)[0]
    image_fname = 'sphx_glr_' + base_image_name + '_{0:03}.png'
    image_path = os.path.join(image_dir, image_fname)

    script_blocks = split_code_and_text_blocks(example_file)

    amount_of_code = sum([len(bcontent)
                          for blabel, bcontent in script_blocks
                          if blabel == 'code'])

    if _plots_are_current(example_file, image_path):
        return amount_of_code

    time_elapsed = 0

    ref_fname = example_file.replace(os.path.sep, '_')
    example_rst = """\n\n.. _sphx_glr_{0}:\n\n""".format(ref_fname)
    example_nb = Notebook(fname, target_dir)

    filename_pattern = gallery_conf.get('filename_pattern')
    if re.search(filename_pattern, src_file) and gallery_conf['plot_gallery']:
        # A lot of examples contains 'print(__doc__)' for example in
        # scikit-learn so that running the example prints some useful
        # information. Because the docstring has been separated from
        # the code blocks in sphinx-gallery, __doc__ is actually
        # __builtin__.__doc__ in the execution context and we do not
        # want to print it
        example_globals = {'__doc__': ''}
        fig_count = 0
        # A simple example has two blocks: one for the
        # example introduction/explanation and one for the code
        is_example_notebook_like = len(script_blocks) > 2
        for blabel, bcontent in script_blocks:
            if blabel == 'code':
                code_output, rtime, fig_count = execute_script(bcontent,
                                                               example_globals,
                                                               image_path,
                                                               fig_count,
                                                               src_file,
                                                               gallery_conf)

                time_elapsed += rtime
                example_nb.add_code_cell(bcontent)

                if is_example_notebook_like:
                    example_rst += codestr2rst(bcontent) + '\n'
                    example_rst += code_output
                else:
                    example_rst += code_output
                    example_rst += codestr2rst(bcontent) + '\n'

            else:
                example_rst += text2string(bcontent) + '\n'
                example_nb.add_markdown_cell(text2string(bcontent))
    else:
        for blabel, bcontent in script_blocks:
            if blabel == 'code':
                example_rst += codestr2rst(bcontent) + '\n'
                example_nb.add_code_cell(bcontent)
            else:
                example_rst += bcontent + '\n'
                example_nb.add_markdown_cell(text2string(bcontent))

    save_thumbnail(image_path, base_image_name, gallery_conf)

    time_m, time_s = divmod(time_elapsed, 60)
    example_nb.save_file()
    with open(os.path.join(target_dir, base_image_name + '.rst'), 'w') as f:
        example_rst += CODE_DOWNLOAD.format(time_m, time_s, fname,
                                            example_nb.file_name)
        f.write(example_rst)

    return amount_of_code