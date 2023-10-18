def version_bump(self, version, type="bug"):
        """
        Increment version number string 'version'.
        
        Type can be one of: major, minor, or bug 
        """
        parsed_version = LooseVersion(version).version
        total_components = max(3, len(parsed_version))
        
        bits = []
        for bit in parsed_version:
            try:
                bit = int(bit)
            except ValueError:
                continue
            
            bits.append(bit)
        
        indexes = {
            "major": 0,
            "minor": 1,
            "bug": 2,
        }
        
        bits += [0] * (3 - len(bits)) # pad to 3 digits
        
        # Increment the version
        bits[indexes[type]] += 1
        
        # Set the subsequent digits to 0
        for i in range(indexes[type] + 1, 3):
            bits[i] = 0
        
        return ".".join(map(str, bits))