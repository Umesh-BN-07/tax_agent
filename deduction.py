class DeductionCalculator:
    def __init__(self, investments):
        self.investments = investments

    def calculate_80C(self):
        return min(self.investments.get("80C", 0), 150000)

    def calculate_80D(self):
        return min(self.investments.get("80D", 0), 25000)

    def total_deductions(self):
        return self.calculate_80C() + self.calculate_80D()