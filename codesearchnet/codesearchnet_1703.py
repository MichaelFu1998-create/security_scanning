def dutyCycle(self, active=False, readOnly=False):
    """Compute/update and return the positive activations duty cycle of
    this segment. This is a measure of how often this segment is
    providing good predictions.

    :param active   True if segment just provided a good prediction

    :param readOnly If True, compute the updated duty cycle, but don't change
               the cached value. This is used by debugging print statements.

    :returns: The duty cycle, a measure of how often this segment is
    providing good predictions.

    **NOTE:** This method relies on different schemes to compute the duty cycle
    based on how much history we have. In order to support this tiered
    approach **IT MUST BE CALLED ON EVERY SEGMENT AT EACH DUTY CYCLE TIER**
    (@ref dutyCycleTiers).

    When we don't have a lot of history yet (first tier), we simply return
    number of positive activations / total number of iterations

    After a certain number of iterations have accumulated, it converts into
    a moving average calculation, which is updated only when requested
    since it can be a bit expensive to compute on every iteration (it uses
    the pow() function).

    The duty cycle is computed as follows:

        dc[t] = (1-alpha) * dc[t-1] + alpha * value[t]

    If the value[t] has been 0 for a number of steps in a row, you can apply
    all of the updates at once using:

        dc[t] = (1-alpha)^(t-lastT) * dc[lastT]

    We use the alphas and tiers as defined in @ref dutyCycleAlphas and
    @ref dutyCycleTiers.
    """
    # For tier #0, compute it from total number of positive activations seen
    if self.tm.lrnIterationIdx <= self.dutyCycleTiers[1]:
      dutyCycle = float(self.positiveActivations) \
                                    / self.tm.lrnIterationIdx
      if not readOnly:
        self._lastPosDutyCycleIteration = self.tm.lrnIterationIdx
        self._lastPosDutyCycle = dutyCycle
      return dutyCycle

    # How old is our update?
    age = self.tm.lrnIterationIdx - self._lastPosDutyCycleIteration

    # If it's already up to date, we can returned our cached value.
    if age == 0 and not active:
      return self._lastPosDutyCycle

    # Figure out which alpha we're using
    for tierIdx in range(len(self.dutyCycleTiers)-1, 0, -1):
      if self.tm.lrnIterationIdx > self.dutyCycleTiers[tierIdx]:
        alpha = self.dutyCycleAlphas[tierIdx]
        break

    # Update duty cycle
    dutyCycle = pow(1.0-alpha, age) * self._lastPosDutyCycle
    if active:
      dutyCycle += alpha

    # Update cached values if not read-only
    if not readOnly:
      self._lastPosDutyCycleIteration = self.tm.lrnIterationIdx
      self._lastPosDutyCycle = dutyCycle

    return dutyCycle