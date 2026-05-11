class AttributePackage:
    @staticmethod
    def calculate(base_value, level, gain_rate, multiplier):
        return int((base_value + (level * gain_rate)) * multiplier)
