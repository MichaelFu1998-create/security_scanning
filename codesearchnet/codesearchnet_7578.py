def execute_script(code_block, example_globals, image_path, fig_count,
                   src_file, gallery_conf):
    """Executes the code block of the example file"""
    time_elapsed = 0
    stdout = ''

    # We need to execute the code
    print('plotting code blocks in %s' % src_file)

    plt.close('all')
    cwd = os.getcwd()
    # Redirect output to stdout and
    orig_stdout = sys.stdout

    try:
        # First cd in the original example dir, so that any file
        # created by the example get created in this directory
        os.chdir(os.path.dirname(src_file))
        my_buffer = StringIO()
        my_stdout = Tee(sys.stdout, my_buffer)
        sys.stdout = my_stdout

        t_start = time()
        exec(code_block, example_globals)
        time_elapsed = time() - t_start

        sys.stdout = orig_stdout

        my_stdout = my_buffer.getvalue().strip().expandtabs()
        if my_stdout:
            stdout = CODE_OUTPUT.format(indent(my_stdout, ' ' * 4))
        os.chdir(cwd)
        figure_list = save_figures(image_path, fig_count, gallery_conf)

        # Depending on whether we have one or more figures, we're using a
        # horizontal list or a single rst call to 'image'.
        image_list = ""
        if len(figure_list) == 1:
            figure_name = figure_list[0]
            image_list = SINGLE_IMAGE % figure_name.lstrip('/')
        elif len(figure_list) > 1:
            image_list = HLIST_HEADER
            for figure_name in figure_list:
                image_list += HLIST_IMAGE_TEMPLATE % figure_name.lstrip('/')

    except Exception:
        formatted_exception = traceback.format_exc()

        print(80 * '_')
        print('%s is not compiling:' % src_file)
        print(formatted_exception)
        print(80 * '_')

        figure_list = []
        image_list = codestr2rst(formatted_exception, lang='pytb')

        # Overrides the output thumbnail in the gallery for easy identification
        broken_img = os.path.join(glr_path_static(), 'broken_example.png')
        shutil.copyfile(broken_img, os.path.join(cwd, image_path.format(1)))
        fig_count += 1  # raise count to avoid overwriting image

        # Breaks build on first example error

        if gallery_conf['abort_on_example_error']:
            raise

    finally:
        os.chdir(cwd)
        sys.stdout = orig_stdout

    print(" - time elapsed : %.2g sec" % time_elapsed)
    code_output = "\n{0}\n\n{1}\n\n".format(image_list, stdout)

    return code_output, time_elapsed, fig_count + len(figure_list)