def function_selector(method_name_and_signature):
        """
        Makes a function hash id from a method signature
        """
        s = sha3.keccak_256()
        s.update(method_name_and_signature.encode())
        return bytes(s.digest()[:4])