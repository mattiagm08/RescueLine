class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint, outputLimits=(-255, 255)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.outputLimits = outputLimits
        self._integral = 0
        self._lastError = 0
        self._lastTime = 0
        self._lastOutput = 0

    def compute(self, currentValue, currentTime):
        if self._lastTime == 0:
            self._lastTime = currentTime
            self._lastError = self.setpoint - currentValue
            return 0

        error = self.setpoint - currentValue
        dt = currentTime - self._lastTime
        
        if dt == 0:
            return self._lastOutput

        P = self.Kp * error

        self._integral += error * dt
        self._integral = self._clamp(self._integral, self.outputLimits[0] / self.Ki, self.outputLimits[1] / self.Ki)
        I = self.Ki * self._integral

        derivative = (error - self._lastError) / dt
        D = self.Kd * derivative

        output = P + I + D

        output = self._clamp(output, self.outputLimits[0], self.outputLimits[1])

        self._lastError = error
        self._lastTime = currentTime
        self._lastOutput = output

        return output

    def _clamp(self, value, lowerBound, upperBound):
        return max(lowerBound, min(value, upperBound))

    def reset(self):
        self._integral = 0
        self._lastError = 0
        self._lastTime = 0
        self._lastOutput = 0