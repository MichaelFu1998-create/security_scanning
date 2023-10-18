def convert_images(image_list):
    """Convert list of images to PNG format.

    @param: image_list ([string, string, ...]): the list of image files
        extracted from the tarball in step 1

    @return: image_list ([str, str, ...]): The list of image files when all
        have been converted to PNG format.
    """
    png_output_contains = 'PNG image'
    ret_list = []
    for image_file in image_list:
        if os.path.isdir(image_file):
            continue

        dummy1, cmd_out, dummy2 = run_shell_command('file %s', (image_file,))
        if cmd_out.find(png_output_contains) > -1:
            ret_list.append(image_file)
        else:
            # we're just going to assume that ImageMagick can convert all
            # the image types that we may be faced with
            # for sure it can do EPS->PNG and JPG->PNG and PS->PNG
            # and PSTEX->PNG
            converted_image_file = get_converted_image_name(image_file)
            cmd_list = ['convert', image_file, converted_image_file]
            dummy1, cmd_out, cmd_err = run_shell_command(cmd_list)
            if cmd_err == '':
                ret_list.append(converted_image_file)
            else:
                raise Exception(cmd_err)
    return ret_list