def write_creation_info(creation_info, out):
    """
    Write the creation info to out.
    """
    out.write('# Creation Info\n\n')
    # Write sorted creators
    for creator in sorted(creation_info.creators):
        write_value('Creator', creator, out)

    # write created
    write_value('Created', creation_info.created_iso_format, out)
    # possible comment
    if creation_info.has_comment:
        write_text_value('CreatorComment', creation_info.comment, out)