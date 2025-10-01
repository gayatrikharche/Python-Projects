class Employee:
    def __init__(self, name, emp_id):
        self.name = name
        self.emp_id = emp_id

    def compute_pay(self, period="monthly"):
        return 0.0

    def apply_raise(self, percent):
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.emp_id} {self.name}>"


class HourlyEmployee(Employee):
    def __init__(self, name, emp_id, hourly_rate):
        super().__init__(name, emp_id)
        self.hourly_rate = float(hourly_rate)
        self.hours_worked = 0.0

    def add_hours(self, hours):
        self.hours_worked += float(hours)

    def compute_pay(self, period="weekly"):
        regular = min(self.hours_worked, 40.0)
        overtime = max(self.hours_worked - 40.0, 0.0)
        pay = regular * self.hourly_rate + overtime * self.hourly_rate * 1.5
        self.hours_worked = 0.0
        return round(pay, 2)

    def apply_raise(self, percent):
        self.hourly_rate *= (1.0 + percent / 100.0)
        self.hourly_rate = round(self.hourly_rate, 2)


class SalariedEmployee(Employee):
    PERIODS_PER_YEAR = {"weekly": 52, "biweekly": 26, "monthly": 12, "annual": 1}

    def __init__(self, name, emp_id, annual_salary):
        super().__init__(name, emp_id)
        self.annual_salary = float(annual_salary)

    def compute_pay(self, period="monthly"):
        return round(self.annual_salary / self.PERIODS_PER_YEAR[period], 2)

    def apply_raise(self, percent):
        self.annual_salary *= (1.0 + percent / 100.0)
        self.annual_salary = round(self.annual_salary, 2)


class Manager(SalariedEmployee):
    def __init__(self, name, emp_id, annual_salary, bonus_percent=10.0):
        super().__init__(name, emp_id, annual_salary)
        self.bonus_percent = float(bonus_percent)

    def compute_pay(self, period="monthly"):
        base = super().compute_pay(period)
        annual_bonus = self.annual_salary * (self.bonus_percent / 100.0)
        per_period_bonus = round(annual_bonus / self.PERIODS_PER_YEAR[period], 2)
        return round(base + per_period_bonus, 2)


class Executive(Manager):
    def __init__(self, name, emp_id, annual_salary, bonus_percent=20.0, equity_cash_per_year=0.0):
        super().__init__(name, emp_id, annual_salary, bonus_percent)
        self.equity_cash_per_year = float(equity_cash_per_year)

    def compute_pay(self, period="monthly"):
        base_plus_bonus = super().compute_pay(period)
        per_period_equity = round(self.equity_cash_per_year / self.PERIODS_PER_YEAR[period], 2)
        return round(base_plus_bonus + per_period_equity, 2)


class Company:
    def __init__(self, name):
        self.name = name
        self._employees = {}

    def hire(self, employee):
        if employee.emp_id in self._employees:
            raise ValueError(f"Employee ID '{employee.emp_id}' already exists.")
        self._employees[employee.emp_id] = employee

    def fire(self, emp_id):
        if emp_id not in self._employees:
            raise ValueError(f"No such employee: {emp_id}")
        return self._employees.pop(emp_id)

    def get(self, emp_id):
        if emp_id not in self._employees:
            raise ValueError(f"No such employee: {emp_id}")
        return self._employees[emp_id]

    def list_employees(self):
        return list(self._employees.values())

    def give_raise(self, emp_id, percent):
        emp = self.get(emp_id)
        emp.apply_raise(percent)

    def run_payroll(self, period="monthly"):
        detail = {}
        total = 0.0
        for emp_id, emp in self._employees.items():
            pay = emp.compute_pay(period=period)
            detail[emp_id] = pay
            total += pay
        return detail, round(total, 2)


if __name__ == "__main__":
    acme = Company("ACME Inc.")
    e1 = HourlyEmployee("Sam Hourly", "H001", 25.0)
    e1.add_hours(42)
    e2 = SalariedEmployee("Sara Salary", "S001", 90000)
    e3 = Manager("Manny Manager", "M001", 120000, 12.0)
    e4 = Executive("Eve Exec", "E001", 200000, 25.0, 60000)
    for e in (e1, e2, e3, e4):
        acme.hire(e)
    acme.give_raise("S001", 5.0)
    detail, total = acme.run_payroll("monthly")
    print(f"Payroll for {acme.name} (monthly):")
    for emp in acme.list_employees():
        print(f"  {emp.emp_id:<4} {emp.name:<15} -> ${detail[emp.emp_id]:,.2f}")
    print(f"Total payroll: ${total:,.2f}")
    fired = acme.fire("H001")
    print(f"Fired: {fired.name} ({fired.emp_id})")
