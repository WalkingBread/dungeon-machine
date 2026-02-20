class Percent:
    def __init__(self, value: float):
        self._value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value: float):
        self._value = max(0.0, min(float(new_value), 1.0))

    def __repr__(self):
        return f"{self._value * 100:.1f}%"