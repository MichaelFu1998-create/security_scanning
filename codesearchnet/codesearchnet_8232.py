def make_matrix_coord_map(
        dx, dy, serpentine=True, offset=0, rotation=0, y_flip=False):
    """Helper method to generate X,Y coordinate maps for strips"""
    result = []
    for y in range(dy):
        if not serpentine or y % 2 == 0:
            result.append([(dx * y) + x + offset for x in range(dx)])
        else:
            result.append([dx * (y + 1) - 1 - x + offset for x in range(dx)])

    result = rotate_and_flip(result, rotation, y_flip)

    return result