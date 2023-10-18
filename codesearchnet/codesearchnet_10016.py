def _create_buffers(self, number):
        """
        Creates a SecBufferDesc struct and contained SecBuffer structs

        :param number:
            The number of contains SecBuffer objects to create

        :return:
            A tuple of (SecBufferDesc pointer, SecBuffer array)
        """

        buffers = new(secur32, 'SecBuffer[%d]' % number)

        for index in range(0, number):
            buffers[index].cbBuffer = 0
            buffers[index].BufferType = Secur32Const.SECBUFFER_EMPTY
            buffers[index].pvBuffer = null()

        sec_buffer_desc_pointer = struct(secur32, 'SecBufferDesc')
        sec_buffer_desc = unwrap(sec_buffer_desc_pointer)

        sec_buffer_desc.ulVersion = Secur32Const.SECBUFFER_VERSION
        sec_buffer_desc.cBuffers = number
        sec_buffer_desc.pBuffers = buffers

        return (sec_buffer_desc_pointer, buffers)