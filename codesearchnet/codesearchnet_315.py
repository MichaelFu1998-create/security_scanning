def blur_gaussian_(image, sigma, ksize=None, backend="auto", eps=1e-3):
    """
    Blur an image using gaussian blurring.

    This operation might change the input image in-place.

    dtype support::

        if (backend="auto")::

            * ``uint8``: yes; fully tested (1)
            * ``uint16``: yes; tested (1)
            * ``uint32``: yes; tested (2)
            * ``uint64``: yes; tested (2)
            * ``int8``: yes; tested (1)
            * ``int16``: yes; tested (1)
            * ``int32``: yes; tested (1)
            * ``int64``: yes; tested (2)
            * ``float16``: yes; tested (1)
            * ``float32``: yes; tested (1)
            * ``float64``: yes; tested (1)
            * ``float128``: no
            * ``bool``: yes; tested (1)

            - (1) Handled by ``cv2``. See ``backend="cv2"``.
            - (2) Handled by ``scipy``. See ``backend="scipy"``.

        if (backend="cv2")::

            * ``uint8``: yes; fully tested
            * ``uint16``: yes; tested
            * ``uint32``: no (2)
            * ``uint64``: no (3)
            * ``int8``: yes; tested (4)
            * ``int16``: yes; tested
            * ``int32``: yes; tested (5)
            * ``int64``: no (6)
            * ``float16``: yes; tested (7)
            * ``float32``: yes; tested
            * ``float64``: yes; tested
            * ``float128``: no (8)
            * ``bool``: yes; tested (1)

            - (1) Mapped internally to ``float32``. Otherwise causes ``TypeError: src data type = 0 is not supported``.
            - (2) Causes ``TypeError: src data type = 6 is not supported``.
            - (3) Causes ``cv2.error: OpenCV(3.4.5) (...)/filter.cpp:2957: error: (-213:The function/feature is not
                  implemented) Unsupported combination of source format (=4), and buffer format (=5) in function
                  'getLinearRowFilter'``.
            - (4) Mapped internally to ``int16``. Otherwise causes ``cv2.error: OpenCV(3.4.5) (...)/filter.cpp:2957:
                  error: (-213:The function/feature is not implemented) Unsupported combination of source format (=1),
                  and buffer format (=5) in function 'getLinearRowFilter'``.
            - (5) Mapped internally to ``float64``. Otherwise causes ``cv2.error: OpenCV(3.4.5) (...)/filter.cpp:2957:
                  error: (-213:The function/feature is not implemented) Unsupported combination of source format (=4),
                  and buffer format (=5) in function 'getLinearRowFilter'``.
            - (6) Causes ``cv2.error: OpenCV(3.4.5) (...)/filter.cpp:2957: error: (-213:The function/feature is not
                  implemented) Unsupported combination of source format (=4), and buffer format (=5) in function
                  'getLinearRowFilter'``.
            - (7) Mapped internally to ``float32``. Otherwise causes ``TypeError: src data type = 23 is not supported``.
            - (8) Causes ``TypeError: src data type = 13 is not supported``.


        if (backend="scipy")::

            * ``uint8``: yes; fully tested
            * ``uint16``: yes; tested
            * ``uint32``: yes; tested
            * ``uint64``: yes; tested
            * ``int8``: yes; tested
            * ``int16``: yes; tested
            * ``int32``: yes; tested
            * ``int64``: yes; tested
            * ``float16``: yes; tested (1)
            * ``float32``: yes; tested
            * ``float64``: yes; tested
            * ``float128``: no (2)
            * ``bool``: yes; tested (3)

            - (1) Mapped internally to ``float32``. Otherwise causes ``RuntimeError: array type dtype('float16')
                  not supported``.
            - (2) Causes ``RuntimeError: array type dtype('float128') not supported``.
            - (3) Mapped internally to ``float32``. Otherwise too inaccurate.

    Parameters
    ----------
    image : numpy.ndarray
        The image to blur. Expected to be of shape ``(H, W)`` or ``(H, W, C)``.

    sigma : number
        Standard deviation of the gaussian blur. Larger numbers result in more large-scale blurring, which is overall
        slower than small-scale blurring.

    ksize : None or int, optional
        Size in height/width of the gaussian kernel. This argument is only understood by the ``cv2`` backend.
        If it is set to None, an appropriate value for `ksize` will automatically be derived from `sigma`.
        The value is chosen tighter for larger sigmas to avoid as much as possible very large kernel sizes
        and therey improve performance.

    backend : {'auto', 'cv2', 'scipy'}, optional
        Backend library to use. If ``auto``, then the likely best library will be automatically picked per image. That
        is usually equivalent to ``cv2`` (OpenCV) and it will fall back to ``scipy`` for datatypes not supported by
        OpenCV.

    eps : number, optional
        A threshold used to decide whether `sigma` can be considered zero.

    Returns
    -------
    image : numpy.ndarray
        The blurred image. Same shape and dtype as the input.

    """
    if sigma > 0 + eps:
        dtype = image.dtype

        iadt.gate_dtypes(image,
                         allowed=["bool",
                                  "uint8", "uint16", "uint32",
                                  "int8", "int16", "int32", "int64", "uint64",
                                  "float16", "float32", "float64"],
                         disallowed=["uint128", "uint256",
                                     "int128", "int256",
                                     "float96", "float128", "float256"],
                         augmenter=None)

        dts_not_supported_by_cv2 = ["uint32", "uint64", "int64", "float128"]
        backend_to_use = backend
        if backend == "auto":
            backend_to_use = "cv2" if image.dtype.name not in dts_not_supported_by_cv2 else "scipy"
        elif backend == "cv2":
            assert image.dtype.name not in dts_not_supported_by_cv2,\
                ("Requested 'cv2' backend, but provided %s input image, which "
                 + "cannot be handled by that backend. Choose a different backend or "
                 + "set backend to 'auto' or use a different datatype.") % (image.dtype.name,)
        elif backend == "scipy":
            # can handle all dtypes that were allowed in gate_dtypes()
            pass

        if backend_to_use == "scipy":
            if dtype.name == "bool":
                # We convert bool to float32 here, because gaussian_filter() seems to only return True when
                # the underlying value is approximately 1.0, not when it is above 0.5. So we do that here manually.
                # cv2 does not support bool for gaussian blur
                image = image.astype(np.float32, copy=False)
            elif dtype.name == "float16":
                image = image.astype(np.float32, copy=False)

            # gaussian_filter() has no ksize argument
            # TODO it does have a truncate argument that truncates at x standard deviations -- maybe can be used
            #      similarly to ksize
            if ksize is not None:
                warnings.warn("Requested 'scipy' backend or picked it automatically by backend='auto' "
                              "in blur_gaussian_(), but also provided 'ksize' argument, which is not understood by "
                              "that backend and will be ignored.")

            # Note that while gaussian_filter can be applied to all channels at the same time, that should not
            # be done here, because then the blurring would also happen across channels (e.g. red values might
            # be mixed with blue values in RGB)
            if image.ndim == 2:
                image[:, :] = ndimage.gaussian_filter(image[:, :], sigma, mode="mirror")
            else:
                nb_channels = image.shape[2]
                for channel in sm.xrange(nb_channels):
                    image[:, :, channel] = ndimage.gaussian_filter(image[:, :, channel], sigma, mode="mirror")
        else:
            if dtype.name == "bool":
                image = image.astype(np.float32, copy=False)
            elif dtype.name == "float16":
                image = image.astype(np.float32, copy=False)
            elif dtype.name == "int8":
                image = image.astype(np.int16, copy=False)
            elif dtype.name == "int32":
                image = image.astype(np.float64, copy=False)

            # ksize here is derived from the equation to compute sigma based on ksize,
            # see https://docs.opencv.org/3.1.0/d4/d86/group__imgproc__filter.html -> cv::getGaussianKernel()
            # example values:
            #   sig = 0.1 -> ksize = -1.666
            #   sig = 0.5 -> ksize = 0.9999
            #   sig = 1.0 -> ksize = 1.0
            #   sig = 2.0 -> ksize = 11.0
            #   sig = 3.0 -> ksize = 17.666
            # ksize = ((sig - 0.8)/0.3 + 1)/0.5 + 1

            if ksize is None:
                if sigma < 3.0:
                    ksize = 3.3 * sigma  # 99% of weight
                elif sigma < 5.0:
                    ksize = 2.9 * sigma  # 97% of weight
                else:
                    ksize = 2.6 * sigma  # 95% of weight

                # we use 5x5 here as the minimum size as that simplifies comparisons with gaussian_filter() in the tests
                # TODO reduce this to 3x3
                ksize = int(max(ksize, 5))
            else:
                assert ia.is_single_integer(ksize), "Expected 'ksize' argument to be a number, got %s." % (type(ksize),)

            ksize = ksize + 1 if ksize % 2 == 0 else ksize

            if ksize > 0:
                image_warped = cv2.GaussianBlur(image, (ksize, ksize), sigmaX=sigma, sigmaY=sigma,
                                                borderType=cv2.BORDER_REFLECT_101)

                # re-add channel axis removed by cv2 if input was (H, W, 1)
                image = image_warped[..., np.newaxis] if image.ndim == 3 and image_warped.ndim == 2 else image_warped

        if dtype.name == "bool":
            image = image > 0.5
        elif dtype.name != image.dtype.name:
            image = iadt.restore_dtypes_(image, dtype)

    return image