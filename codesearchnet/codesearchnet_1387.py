def run(self):
    """Run the spatial pooler with the input vector"""

    print "-" * 80 + "Computing the SDR" + "-" * 80

    #activeArray[column]=1 if column is active after spatial pooling
    self.sp.compute(self.inputArray, True, self.activeArray)

    print self.activeArray.nonzero()