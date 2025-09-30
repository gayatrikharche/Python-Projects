from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

class Employee(ABC):
    def __init__(self, name: str, emp_id: str):
        self.name = name
        self.emp_id = emp_id

    @abstractmethod
    def compute_pay(self, period: str = "monthly") -> float:
        """Return gross pay for this pay period."""

    @abstractmethod
    def apply_raise(self, percent: float) -> None:
        """Apply a raise (e.g., 5.0 for 5%)."""

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.emp_id} {self.name}>"


class HourlyEmployee(Employee):
    """
    Overtime rule: >40 hours in a period paid at 1.5x.
    Hours reset to 0 after payroll.
    """
    def __init__(self, name: str, emp_id: str, hourly_rate: float):
        super().__init__(name, emp_id)
        self.hourly_rate = float(hourly_rate)
        self.hours_worked = 0.0

    def add_hours(self, hours: float) -> None:
        self.hours_worked += float(hours)

    def compute_pay(self, period: str = "weekly") -> float:
        regular = min(self.hours_worked, 40.0)
        overtime = max(self.hours_worked - 40.0, 0.0)
        pay = regular * self.hourly_rate + overtime * self.hourly_rate * 1.5
        # Reset hours after paying out
        self.hours_worked = 0.0
        return round(pay, 2)

    def apply_raise(self, percent: float) -> None:
        self.hourly_rate *= (1.0 + percent / 100.0)
        self.hourly_rate = round(self.hourly_rate, 2)


class SalariedEmployee(Employee):
    """
    Salary is pro-rated by period.
    Supported periods: 'weekly', 'biweekly', 'monthly', 'annual'
    """
    PERIODS_PER_YEAR = {
        "weekly": 52,
        "biweekly": 26,
        "monthly": 12,
        "annual": 1,
    }

    def __init__(self, name: str, emp_id: str, annual_salary: float):
        super().__init__(name, emp_id)
        self.annual_salary = float(annual_salary)

    def compute_pay(self, period: str = "monthly") -> float:
        if period not in self.PERIODS_PER_YEAR:
            raise ValueError(f"Unsupported period: {period}")
        return round(self.annual_salary / self.PERIODS_PER_YEAR[period], 2)

    def apply_raise(self, percent: float) -> None:
        self.annual_salary *= (1.0 + percent / 100.0)
        self.annual_salary = round(self.annual_salary, 2)


class Manager(SalariedEmployee):
    """
    Managers get salary + a periodic bonus (as a percent of salary).
    Bonus is annualized and pro-rated to the pay period.
    """
    def __init__(self, name: str, emp_id: str, annual_salary: float, bonus_percent: float = 10.0):
        super().__init__(name, emp_id, annual_salary)
        self.bonus_percent = float(bonus_percent)

    def compute_pay(self, period: str = "monthly") -> float:
        base = super().compute_pay(period)
        annual_bonus = self.annual_salary * (self.bonus_percent / 100.0)
        per_period_bonus = round(annual_bonus / self.PERIODS_PER_YEAR[period], 2)
        return round(base + per_period_bonus, 2)


class Executive(Manager):
    """
    Executives get salary + bonus + equity cash value (annualized).
    """
    def __init__(self, name: str, emp_id: str, annual_salary: float,
                 bonus_percent: float = 20.0, equity_cash_per_year: float = 0.0):
        super().__init__(name, emp_id, annual_salary, bonus_percent)
        self.equity_cash_per_year = float(equity_cash_per_year)

    def compute_pay(self, period: str = "monthly") -> float:
        base_plus_bonus = super().compute_pay(period)
        per_period_equity = round(self.equity_cash_per_year / self.PERIODS_PER_YEAR[period], 2)
        return round(base_plus_bonus + per_period_equity, 2)


# ---------- Company Management ----------

class Company:
    def __init__(self, name: str):
        self.name = name
        self._employees: Dict[str, Employee] = {}

    # Hire / fire
    def hire(self, employee: Employee) -> None:
        if employee.emp_id in self._employees:
            raise ValueError(f"Employee ID '{employee.emp_id}' already exists.")
        self._employees[employee.emp_id] = employee

    def fire(self, emp_id: str) -> Employee:
        try:
            return self._employees.pop(emp_id)
        except KeyError:
            raise ValueError(f"No such employee: {emp_id}")

    # Access
    def get(self, emp_id: str) -> Employee:
        try:
            return self._employees[emp_id]
        except KeyError:
            raise ValueError(f"No such employee: {emp_id}")

    def list_employees(self) -> List[Employee]:
        return list(self._employees.values())

    # Raises
    def give_raise(self, emp_id: str, percent: float) -> None:
        emp = self.get(emp_id)
        emp.apply_raise(percent)

    # Payroll
    def run_payroll(self, period: str = "monthly") -> Tuple[Dict[str, float], float]:
        """
        Returns (payroll_detail, total_payroll), where payroll_detail maps emp_id -> pay.
        """
        detail: Dict[str, float] = {}
        total = 0.0
        for emp_id, emp in self._employees.items():
            pay = emp.compute_pay(period=period)
            detail[emp_id] = pay
            total += pay
        return detail, round(total, 2)


if __name__ == "__main__":
    # Create company
    acme = Company("ACME Inc.")

    # Hire employees
    e1 = HourlyEmployee("Sam Hourly", "H001", hourly_rate=25.0)
    e1.add_hours(42)  # includes 2 hours overtime this week

    e2 = SalariedEmployee("Sara Salary", "S001", annual_salary=90_000)
    e3 = Manager("Manny Manager", "M001", annual_salary=120_000, bonus_percent=12.0)
    e4 = Executive("Eve Exec", "E001", annual_salary=200_000, bonus_percent=25.0, equity_cash_per_year=60_000)

    for e in (e1, e2, e3, e4):
        acme.hire(e)

    # Give a raise to salaried employee
    acme.give_raise("S001", 5.0)  # 5% raise

    # Run payroll
    detail, total = acme.run_payroll(period="monthly")  # weekly/biweekly/monthly/annual
    print(f"Payroll for {acme.name} (monthly):")
    for emp in acme.list_employees():
        print(f"  {emp.emp_id:<4} {emp.name:<15} -> ${detail[emp.emp_id]:,.2f}")
    print(f"Total payroll: ${total:,.2f}")

    # Fire someone
    fired = acme.fire("H001")
    print(f"Fired: {fired.name} ({fired.emp_id})")

