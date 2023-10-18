def pad(arr, top=0, right=0, bottom=0, left=0, mode="constant", cval=0):
    """
    Pad an image-like array on its top/right/bottom/left side.

    This function is a wrapper around :func:`numpy.pad`.

    dtype support::

        * ``uint8``: yes; fully tested (1)
        * ``uint16``: yes; fully tested (1)
        * ``uint32``: yes; fully tested (2) (3)
        * ``uint64``: yes; fully tested (2) (3)
        * ``int8``: yes; fully tested (1)
        * ``int16``: yes; fully tested (1)
        * ``int32``: yes; fully tested (1)
        * ``int64``: yes; fully tested (2) (3)
        * ``float16``: yes; fully tested (2) (3)
        * ``float32``: yes; fully tested (1)
        * ``float64``: yes; fully tested (1)
        * ``float128``: yes; fully tested (2) (3)
        * ``bool``: yes; tested (2) (3)

        - (1) Uses ``cv2`` if `mode` is one of: ``"constant"``, ``"edge"``, ``"reflect"``, ``"symmetric"``.
              Otherwise uses ``numpy``.
        - (2) Uses ``numpy``.
        - (3) Rejected by ``cv2``.

    Parameters
    ----------
    arr : (H,W) ndarray or (H,W,C) ndarray
        Image-like array to pad.

    top : int, optional
        Amount of pixels to add at the top side of the image. Must be 0 or greater.

    right : int, optional
        Amount of pixels to add at the right side of the image. Must be 0 or greater.

    bottom : int, optional
        Amount of pixels to add at the bottom side of the image. Must be 0 or greater.

    left : int, optional
        Amount of pixels to add at the left side of the image. Must be 0 or greater.

    mode : str, optional
        Padding mode to use. See :func:`numpy.pad` for details.
        In case of mode ``constant``, the parameter `cval` will be used as the ``constant_values``
        parameter to :func:`numpy.pad`.
        In case of mode ``linear_ramp``, the parameter `cval` will be used as the ``end_values``
        parameter to :func:`numpy.pad`.

    cval : number, optional
        Value to use for padding if `mode` is ``constant``. See :func:`numpy.pad` for details.
        The cval is expected to match the input array's dtype and value range.

    Returns
    -------
    arr_pad : (H',W') ndarray or (H',W',C) ndarray
        Padded array with height ``H'=H+top+bottom`` and width ``W'=W+left+right``.

    """
    do_assert(arr.ndim in [2, 3])
    do_assert(top >= 0)
    do_assert(right >= 0)
    do_assert(bottom >= 0)
    do_assert(left >= 0)
    if top > 0 or right > 0 or bottom > 0 or left > 0:
        mapping_mode_np_to_cv2 = {
            "constant": cv2.BORDER_CONSTANT,
            "edge": cv2.BORDER_REPLICATE,
            "linear_ramp": None,
            "maximum": None,
            "mean": None,
            "median": None,
            "minimum": None,
            "reflect": cv2.BORDER_REFLECT_101,
            "symmetric": cv2.BORDER_REFLECT,
            "wrap": None,
            cv2.BORDER_CONSTANT: cv2.BORDER_CONSTANT,
            cv2.BORDER_REPLICATE: cv2.BORDER_REPLICATE,
            cv2.BORDER_REFLECT_101: cv2.BORDER_REFLECT_101,
            cv2.BORDER_REFLECT: cv2.BORDER_REFLECT
        }
        bad_mode_cv2 = mapping_mode_np_to_cv2.get(mode, None) is None

        # these datatypes all simply generate a "TypeError: src data type = X is not supported" error
        bad_datatype_cv2 = arr.dtype.name in ["uint32", "uint64", "int64", "float16", "float128", "bool"]

        if not bad_datatype_cv2 and not bad_mode_cv2:
            cval = float(cval) if arr.dtype.kind == "f" else int(cval)  # results in TypeError otherwise for np inputs

            if arr.ndim == 2 or arr.shape[2] <= 4:
                # without this, only the first channel is padded with the cval, all following channels with 0
                if arr.ndim == 3:
                    cval = tuple([cval] * arr.shape[2])

                arr_pad = cv2.copyMakeBorder(arr, top=top, bottom=bottom, left=left, right=right,
                                             borderType=mapping_mode_np_to_cv2[mode], value=cval)
                if arr.ndim == 3 and arr_pad.ndim == 2:
                    arr_pad = arr_pad[..., np.newaxis]
            else:
                result = []
                channel_start_idx = 0
                while channel_start_idx < arr.shape[2]:
                    arr_c = arr[..., channel_start_idx:channel_start_idx+4]
                    cval_c = tuple([cval] * arr_c.shape[2])
                    arr_pad_c = cv2.copyMakeBorder(arr_c, top=top, bottom=bottom, left=left, right=right,
                                                   borderType=mapping_mode_np_to_cv2[mode], value=cval_c)
                    arr_pad_c = np.atleast_3d(arr_pad_c)
                    result.append(arr_pad_c)
                    channel_start_idx += 4
                arr_pad = np.concatenate(result, axis=2)
        else:
            paddings_np = [(top, bottom), (left, right)]  # paddings for 2d case
            if arr.ndim == 3:
                paddings_np.append((0, 0))  # add paddings for 3d case

            if mode == "constant":
                arr_pad = np.pad(arr, paddings_np, mode=mode, constant_values=cval)
            elif mode == "linear_ramp":
                arr_pad = np.pad(arr, paddings_np, mode=mode, end_values=cval)
            else:
                arr_pad = np.pad(arr, paddings_np, mode=mode)

        return arr_pad
    return np.copy(arr)