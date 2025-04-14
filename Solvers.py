import math

class MastersTheorem:
    def __init__(self, a, b, is_decreasing, k, p=None):
        self.a = a
        self.b = b
        self.is_decreasing = is_decreasing
        self.k = k
        self.p = p

    def get_ans(self):
        result = self._calculate()
        if not result:
            return None

        notation = "O" if self.is_decreasing else "\\Theta"
        return f"{notation}({result})"

    def _calculate(self):
        if self.is_decreasing and self.a > 0 and self.b > 0 and self.k >= 0:
            return self._decreasing_case()
        elif not self.is_decreasing and self.a >= 1 and self.b > 1:
            return self._dividing_case()

    def _decreasing_case(self):
        f_n = f"n^{self.k} log^{self.p}(n)"

        if self.a < 1:
            return f_n
        elif self.a == 1:
            return f"n*{f_n}"
        elif self.a > 1:
            return f"{self.a}^{{n/{self.b}}} {f_n}"

    def _dividing_case(self):
        log_b_a = math.log(self.a, self.b)

        if log_b_a > self.k:
            return f"n^{round(log_b_a, 2)}"
        elif log_b_a == self.k:
            if self.p > -1:
                return f"n^{self.k} log^{self.p + 1}(n)"
            elif self.p == -1:
                return f"n^{self.k} log(log(n))"
            elif self.p < -1:
                return f"n^{self.k}"
        elif log_b_a < self.k:
            if self.p >= 0:
                return f"n^{self.k} log^{self.p}(n)"
            elif self.p < 0:
                return f"n^{self.k}"


class AkraBazzi:
    def __init__(self, terms, k, p):
        """
        Initialize with:
        - terms: list of tuples (a, b) representing a*T(n/b)
        - k: the exponent of n in f(n) = n^k * log^p(n)
        - p: the exponent of log in f(n)
        """
        self.terms = terms
        self.k = k
        self.p = p
        self._p_value = None

    def _characteristic_equation(self, p):
        """Calculate sum(a_i * b_i^(-p)) - 1"""
        return sum(a * (1 / b) ** p for a, b in self.terms) - 1

    def _binary_search_p(self, low=0.1, high=10.0, tol=0.01, max_iter=100):
        """Find root of characteristic equation using binary search"""
        iter_count = 0
        while high - low > tol and iter_count < max_iter:
            mid = (low + high) / 2
            if self._characteristic_equation(mid) * self._characteristic_equation(low) < 0:
                high = mid
            else:
                low = mid
            iter_count += 1

        mid_p = (low + high) / 2
        if abs(self._characteristic_equation(mid_p)) < tol:
            return mid_p
        return None

    def find_p(self):
        """Find the p value that satisfies the characteristic equation"""
        try:
            p_estimate = self._binary_search_p()
            if p_estimate is not None and p_estimate > 0:
                self._p_value = p_estimate
                return p_estimate
            else:
                return None
        except:
            return None

    def get_ans(self):
        """Get the LaTeX formatted answer"""
        p = self._p_value if self._p_value is not None else self.find_p()

        if p is None:
            return None

        if self.k > p:
            return r"\Theta(n^{" + str(self.k) + r"})"
        elif abs(self.k - p) < 0.01:
            return r"\Theta(n^{" + str(self.k) + r"} \log n)"
        else:
            return r"\Theta(n^{" + str(round(p, 2)) + r"})"
