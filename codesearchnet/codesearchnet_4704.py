def small_abc_image_recognition():
    """!
    @brief Trains network using letters 'A', 'B', 'C', and recognize each of them with and without noise.
    
    """
    images = [];
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_A;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_B;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_C;
    
    template_recognition_image(images, 250, 25);