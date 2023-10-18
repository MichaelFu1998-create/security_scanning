def load_glb(self):
        """Loads a binary gltf file"""
        with open(self.path, 'rb') as fd:
            # Check header
            magic = fd.read(4)
            if magic != GLTF_MAGIC_HEADER:
                raise ValueError("{} has incorrect header {} != {}".format(self.path, magic, GLTF_MAGIC_HEADER))

            version = struct.unpack('<I', fd.read(4))[0]
            if version != 2:
                raise ValueError("{} has unsupported version {}".format(self.path, version))

            # Total file size including headers
            _ = struct.unpack('<I', fd.read(4))[0]  # noqa

            # Chunk 0 - json
            chunk_0_length = struct.unpack('<I', fd.read(4))[0]
            chunk_0_type = fd.read(4)
            if chunk_0_type != b'JSON':
                raise ValueError("Expected JSON chunk, not {} in file {}".format(chunk_0_type, self.path))

            json_meta = fd.read(chunk_0_length).decode()

            # chunk 1 - binary buffer
            chunk_1_length = struct.unpack('<I', fd.read(4))[0]
            chunk_1_type = fd.read(4)
            if chunk_1_type != b'BIN\x00':
                raise ValueError("Expected BIN chunk, not {} in file {}".format(chunk_1_type, self.path))

            self.meta = GLTFMeta(self.path, json.loads(json_meta), binary_buffer=fd.read(chunk_1_length))