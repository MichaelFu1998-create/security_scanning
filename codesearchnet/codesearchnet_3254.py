def LEAVE(cpu):
        """
        High level procedure exit.

        Releases the stack frame set up by an earlier ENTER instruction. The
        LEAVE instruction copies the frame pointer (in the EBP register) into
        the stack pointer register (ESP), which releases the stack space allocated
        to the stack frame. The old frame pointer (the frame pointer for the calling
        procedure that was saved by the ENTER instruction) is then popped from
        the stack into the EBP register, restoring the calling procedure's stack
        frame.
        A RET instruction is commonly executed following a LEAVE instruction
        to return program control to the calling procedure::

                IF Stackaddress_bit_size  =  32
                THEN
                    ESP  =  EBP;
                ELSE (* Stackaddress_bit_size  =  16*)
                    SP  =  BP;
                FI;
                IF OperandSize  =  32
                THEN
                    EBP  =  Pop();
                ELSE (* OperandSize  =  16*)
                    BP  =  Pop();
                FI;

        :param cpu: current CPU.
        """
        cpu.STACK = cpu.FRAME
        cpu.FRAME = cpu.pop(cpu.address_bit_size)