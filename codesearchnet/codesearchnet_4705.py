def small_ftk_image_recognition():
    """!
    @brief Trains network using letters 'F', 'T', 'K' and recognize each of them with and without noise.
    
    """
    images = [];
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_F;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_T;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_K;
    
    template_recognition_image(images, 100, 10, 0.2);