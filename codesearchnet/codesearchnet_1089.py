def _initializeEncoders(self, encoderSpec):
    """ Initialize the encoders"""

    #Initializing scalar encoder
    if self.encoderType in ['adaptiveScalar', 'scalar']:
      if 'minval' in encoderSpec:
        self.minval = encoderSpec.pop('minval')
      else: self.minval=None
      if 'maxval' in encoderSpec:
        self.maxval = encoderSpec.pop('maxval')
      else: self.maxval = None
      self.encoder=adaptive_scalar.AdaptiveScalarEncoder(name='AdaptiveScalarEncoder', \
                                                         w=self.w, n=self.n, minval=self.minval, maxval=self.maxval, periodic=False, forced=True)

    #Initializing category encoder
    elif self.encoderType=='category':
      self.encoder=sdr_category.SDRCategoryEncoder(name='categoryEncoder', \
                                                   w=self.w, n=self.n)

    #Initializing date encoder
    elif self.encoderType in ['date', 'datetime']:
      self.encoder=date.DateEncoder(name='dateEncoder')
    else:
      raise RuntimeError('Error in constructing class object. Either encoder type'
          'or dataType must be specified')