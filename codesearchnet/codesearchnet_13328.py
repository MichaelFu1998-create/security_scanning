def check_bidi(data):
        """Checks if sting is valid for bidirectional printing."""
        has_l = False
        has_ral = False
        for char in data:
            if stringprep.in_table_d1(char):
                has_ral = True
            elif stringprep.in_table_d2(char):
                has_l = True
        if has_l and has_ral:
            raise StringprepError("Both RandALCat and LCat characters present")
        if has_ral and (not stringprep.in_table_d1(data[0])
                                    or not stringprep.in_table_d1(data[-1])):
            raise StringprepError("The first and the last character must"
                                                                " be RandALCat")
        return data