def check_glfw_version(self):
        """
        Ensure glfw library  version is compatible
        """
        print("glfw version: {} (python wrapper version {})".format(glfw.get_version(), glfw.__version__))
        if glfw.get_version() < self.min_glfw_version:
            raise ValueError("Please update glfw binaries to version {} or later".format(self.min_glfw_version))