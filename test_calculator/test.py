import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_modulo(self):
        result = self.calculator.evaluate("10 % 3")
        self.assertEqual(result, 1)

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression_1(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_complex_expression_2(self):
        result = self.calculator.evaluate("10 + 2 * 3 - 15 / 5 % 2")
        self.assertEqual(result, 15)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

    def test_factorial(self):
        result = self.calculator.evaluate("5 !")
        self.assertEqual(result, 120)

    def test_factorial_with_other_operators(self):
        result = self.calculator.evaluate("2 * 3 !")
        self.assertEqual(result, 12)

    def test_factorial_invalid_input(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("-5 !")
        with self.assertRaises(ValueError):
            self.calculator.evaluate("5.5 !")


if __name__ == "__main__":
    unittest.main()