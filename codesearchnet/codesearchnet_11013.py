def translate_buffer_format(vertex_format):
    """Translate the buffer format"""
    buffer_format = []
    attributes = []
    mesh_attributes = []

    if "T2F" in vertex_format:
        buffer_format.append("2f")
        attributes.append("in_uv")
        mesh_attributes.append(("TEXCOORD_0", "in_uv", 2))

    if "C3F" in vertex_format:
        buffer_format.append("3f")
        attributes.append("in_color")
        mesh_attributes.append(("NORMAL", "in_color", 3))

    if "N3F" in vertex_format:
        buffer_format.append("3f")
        attributes.append("in_normal")
        mesh_attributes.append(("NORMAL", "in_normal", 3))

    buffer_format.append("3f")
    attributes.append("in_position")
    mesh_attributes.append(("POSITION", "in_position", 3))

    return " ".join(buffer_format), attributes, mesh_attributes