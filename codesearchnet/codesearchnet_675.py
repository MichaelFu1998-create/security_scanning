def save_image(image, image_path='_temp.png'):
    """Save a image.

    Parameters
    -----------
    image : numpy array
        [w, h, c]
    image_path : str
        path

    """
    try:  # RGB
        imageio.imwrite(image_path, image)
    except Exception:  # Greyscale
        imageio.imwrite(image_path, image[:, :, 0])