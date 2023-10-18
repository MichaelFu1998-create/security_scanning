def _element_at_zoom(name, element, zoom):
        """
        Return the element filtered by zoom level.

        - An input integer or float gets returned as is.
        - An input string is checked whether it starts with "zoom". Then, the
          provided zoom level gets parsed and compared with the actual zoom
          level. If zoom levels match, the element gets returned.
        TODOs/gotchas:
        - Elements are unordered, which can lead to unexpected results when
          defining the YAML config.
        - Provided zoom levels for one element in config file are not allowed
          to "overlap", i.e. there is not yet a decision mechanism implemented
          which handles this case.
        """
        # If element is a dictionary, analyze subitems.
        if isinstance(element, dict):
            if "format" in element:
                # we have an input or output driver here
                return element
            out_elements = {}
            for sub_name, sub_element in element.items():
                out_element = _element_at_zoom(sub_name, sub_element, zoom)
                if name == "input":
                    out_elements[sub_name] = out_element
                elif out_element is not None:
                    out_elements[sub_name] = out_element
            # If there is only one subelement, collapse unless it is
            # input. In such case, return a dictionary.
            if len(out_elements) == 1 and name != "input":
                return next(iter(out_elements.values()))
            # If subelement is empty, return None
            if len(out_elements) == 0:
                return None
            return out_elements
        # If element is a zoom level statement, filter element.
        elif isinstance(name, str):
            if name.startswith("zoom"):
                return _filter_by_zoom(
                    conf_string=name.strip("zoom").strip(), zoom=zoom,
                    element=element)
            # If element is a string but not a zoom level statement, return
            # element.
            else:
                return element
        # Return all other types as they are.
        else:
            return element