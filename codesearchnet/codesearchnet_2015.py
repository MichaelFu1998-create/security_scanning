def reverse(self):
        "reverse *IN PLACE*"
        leftblock = self.left
        rightblock = self.right
        leftindex = self.leftndx
        rightindex = self.rightndx
        for i in range(self.length // 2):
            # Validate that pointers haven't met in the middle
            assert leftblock != rightblock or leftindex < rightindex

            # Swap
            (rightblock[rightindex], leftblock[leftindex]) = (
                leftblock[leftindex], rightblock[rightindex])

            # Advance left block/index pair
            leftindex += 1
            if leftindex == n:
                leftblock = leftblock[RGTLNK]
                assert leftblock is not None
                leftindex = 0

            # Step backwards with the right block/index pair
            rightindex -= 1
            if rightindex == -1:
                rightblock = rightblock[LFTLNK]
                assert rightblock is not None
                rightindex = n - 1