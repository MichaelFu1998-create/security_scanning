def getOSName(self):
		"""
		Get the OS name. If OS is linux, returns the Linux distribution name

		Returns:
			str: OS name
		"""
		_system = platform.system()
		if _system in [self.__class__.OS_WINDOWS, self.__class__.OS_MAC, self.__class__.OS_LINUX]:
			if _system == self.__class__.OS_LINUX:
				_dist = platform.linux_distribution()[0]
				if _dist.lower() == self.__class__.OS_UBUNTU.lower():
					return self.__class__.OS_UBUNTU
				elif _dist.lower() == self.__class__.OS_DEBIAN.lower():
					return self.__class__.OS_DEBIAN
				elif _dist.lower() == self.__class__.OS_CENTOS.lower():
					return self.__class__.OS_CENTOS
				elif _dist.lower() == self.__class__.OS_REDHAT.lower():
					return self.__class__.OS_REDHAT
				elif _dist.lower() == self.__class__.OS_KALI.lower():
					return self.__class__.OS_KALI
			return _system
		else:
			return None