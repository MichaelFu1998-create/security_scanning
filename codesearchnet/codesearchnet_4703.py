def small_mind_image_recognition():
    """!
    @brief Trains network using letters 'M', 'I', 'N', 'D' and recognize each of them with and without noise.
    
    """
    images = [];
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_M;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_I;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_N;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_D;
    
    template_recognition_image(images, 100, 10, 0.2);