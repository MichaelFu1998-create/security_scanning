def get_proj(prj_code):
    """
      Helper method for handling projection codes that are unknown to pyproj

      Args:
          prj_code (str): an epsg proj code

      Returns:
          projection: a pyproj projection
    """
    if prj_code in CUSTOM_PRJ:
        proj = pyproj.Proj(CUSTOM_PRJ[prj_code])
    else:
        proj = pyproj.Proj(init=prj_code)
    return proj