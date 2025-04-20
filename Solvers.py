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
        return f'{"O" if self.is_decreasing else r"\Theta"}({result})'

    def _calculate(self):
        if self.is_decreasing and self.a > 0 and self.b > 0 and self.k >= 0:
            return self._decreasing_case()
        elif not self.is_decreasing and self.a >= 1 and self.b > 1:
            return self._dividing_case()

    def _decreasing_case(self):
        f_n = rf"n^{{{self.k}}} \log^{{{self.p}}}(n)"

        if self.a < 1:
            return f_n
        elif self.a == 1:
            return rf"n*{f_n}"
        elif self.a > 1:
            return rf"{self.a}^{{n/{self.b}}} {f_n}"

    def _dividing_case(self):
        log_b_a = math.log(self.a, self.b)
        base_factor = rf"n^{{{self.k}}}"

        if log_b_a > self.k:
            return rf"n^{{{log_b_a:.1f}}}"
        elif log_b_a == self.k:
            if self.p > -1:
                return rf"{base_factor} \log^{{{self.p + 1}}}(n)"
            elif self.p == -1:
                return rf"{base_factor} \log(\log(n))"
            elif self.p < -1:
                return base_factor
        elif log_b_a < self.k:
            if self.p >= 0:
                return rf"{base_factor} \log^{{{self.p}}}(n)"
            elif self.p < 0:
                return base_factor


class AkraBazzi:
    def __init__(self, terms, k, p):
        self.terms = terms
        self.k = k
        self.p = p
        self._p_value = None
        self.tol = 0.01

    def get_ans(self):
        result = self._calculate()
        if not result:
            return None
        return rf"\Theta({result})"

    def _get_sum(self, p):
        return sum(a * (1 / b) ** p for a, b in self.terms) - 1

    def _find_p(self, low=0.1, high=10.0, max_iter=100):
        iter_count = 0
        while high - low > self.tol and iter_count < max_iter:
            iter_count += 1
            mid = (low + high) / 2
            if self._get_sum(mid) * self._get_sum(low) < 0:
                high = mid
            else:
                low = mid

        mid_p = (low + high) / 2
        if abs(self._get_sum(mid_p)) < self.tol:
            return mid_p

        return None

    def _calculate(self):
        # T(n) = Θ(n^p · (1 + ∫₁ⁿ (g(u)/u^(p+1)) du))
        self._p_value = self._find_p()
        if not (self._p_value is not None and self._p_value >= 0):
            return None
        
        diff = self.k - self._p_value
        base_factor = rf"n^{{{self._p_value:.1f}}}"

        if diff > self.tol:
            return rf"{base_factor} n^{{{diff:.1f}}}"
        elif abs(diff) <= self.tol:
            if self.p == 0:
                return rf"{base_factor} \log(n)"
            elif self.p > 0:
                return rf"{base_factor} \log^{{{self.p+1}}}(n)"
            elif self.p == -1:
                return rf"{base_factor} \log(\log(n))"
            elif self.p < -1:
                return base_factor
        elif diff < -self.tol:
            return base_factor