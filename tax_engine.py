class TaxCalculator:
    def __init__(self, income, deductions=0, regime="new"):
        self.income = income
        self.deductions = deductions
        self.regime = regime

    def taxable_income(self):
        standard_deduction = 50000
        if self.regime == "old":
            return max(0, self.income - standard_deduction - self.deductions)
        else:
            return max(0, self.income - standard_deduction)

    def calculate_tax(self):
        income = self.taxable_income()
        tax = 0

        if self.regime == "new":
            slabs = [
                (400000, 0.0),
                (800000, 0.05),
                (1200000, 0.10),
                (1600000, 0.15),
                (2000000, 0.20),
                (2400000, 0.25),
                (float('inf'), 0.30),
            ]
        else:
            slabs = [
                (250000, 0.0),
                (500000, 0.05),
                (1000000, 0.20),
                (float('inf'), 0.30),
            ]

        prev_limit = 0

        for limit, rate in slabs:
            if income > limit:
                tax += (limit - prev_limit) * rate
                prev_limit = limit
            else:
                tax += (income - prev_limit) * rate
                break

        tax *= 1.04  # 4% cess
        return round(tax, 2)