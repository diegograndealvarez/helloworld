import pytest
import unittest

from app.calc import Calculator


@pytest.mark.unit
class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_method_returns_correct_result(self):
        # Comprova el funcionament correcte del mètode add amb valors positius,
        # negatius i el valor límit zero
        self.assertEqual(4, self.calc.add(2, 2))
        self.assertEqual(0, self.calc.add(2, -2))
        self.assertEqual(0, self.calc.add(-2, 2))
        self.assertEqual(1, self.calc.add(1, 0))

    def test_add_method_returns_correct_result1(self):
        # Comprova de nou el mètode add amb altres valors vàlids
        # Aquest test reforça la cobertura del camí principal del mètode
        self.assertEqual(6, self.calc.add(3, 3))
        self.assertEqual(0, self.calc.add(2, -2))
        self.assertEqual(0, self.calc.add(-2, 2))
        self.assertEqual(1, self.calc.add(1, 0))      
        
    def test_divide_method_returns_correct_result(self):
        # Comprova el funcionament correcte del mètode divide amb divisions vàlides
        # També valida el control de tipus quan els paràmetres no són numèrics
        self.assertEqual(1, self.calc.divide(2, 2))
        self.assertEqual(1.5, self.calc.divide(3, 2))
        self.assertRaises(TypeError, self.calc.divide, "2", 2)
  
    def test_add_method_fails_with_nan_parameter(self):
        # Comprova que el mètode add rebutja correctament paràmetres no numèrics
        # Aquest test cobreix la validació de tipus del mètode check_types()
        self.assertRaises(TypeError, self.calc.add, "2", 2)
        self.assertRaises(TypeError, self.calc.add, 2, "2")
        self.assertRaises(TypeError, self.calc.add, "2", "2")
        self.assertRaises(TypeError, self.calc.add, None, 2)
        self.assertRaises(TypeError, self.calc.add, 2, None)
        self.assertRaises(TypeError, self.calc.add, object(), 2)
        self.assertRaises(TypeError, self.calc.add, 2, object())
    
    def test_divide_method_fails_with_nan_parameter(self):
        # Comprova que el mètode divide rebutja paràmetres no numèrics
        # i llança una excepció quan els tipus no són vàlids
        self.assertRaises(TypeError, self.calc.divide, "2", 2)
        self.assertRaises(TypeError, self.calc.divide, 2, "2")
        self.assertRaises(TypeError, self.calc.divide, "2", "2")

    def test_multiply_method_returns_correct_result(self):
        # Comprova el funcionament correcte del mètode multiply
        # incloent valors negatius i el valor límit zero
        self.assertEqual(4, self.calc.multiply(2, 2))
        self.assertEqual(0, self.calc.multiply(1, 0))
        self.assertEqual(0, self.calc.multiply(-1, 0))
        self.assertEqual(-2, self.calc.multiply(-1, 2))
        self.assertRaises(TypeError, self.calc.multiply, "0", 0)
        
    def test_power_method_returns_correct_result(self):
        # Comprova el càlcul correcte de potències amb diferents valors
        # incloent exponents zero i bases negatives
        self.assertEqual(4, self.calc.power(2, 2))
        self.assertEqual(1, self.calc.power(1, 0))
        self.assertEqual(1, self.calc.power(-1, 0))
        self.assertEqual(-27, self.calc.power(-3, 3))
        self.assertRaises(TypeError, self.calc.power, "0", 0)
        
    def test_substract_method_returns_correct_result(self):
        # Comprova el funcionament correcte del mètode substract
        # amb valors positius, negatius i el valor límit zero
        self.assertEqual(4, self.calc.substract(10, 6))
        self.assertEqual(-2, self.calc.substract(256, 258))
        self.assertEqual(-1, self.calc.substract(-1, 0))
        self.assertEqual(0, self.calc.substract(0, 0))
        self.assertEqual(0, self.calc.substract(0, 0))
        self.assertRaises(TypeError, self.calc.substract, "0", 0)

# Reto 3

    def test_divide_by_zero_raises_type_error(self):
        # Comprova que la divisió per zero genera una excepció de tipus TypeError
        # Aquest test cobreix la branca on y == 0 dins del mètode divide()
    with self.assertRaises(TypeError):
        self.calc.divide(10, 0)
    
    def test_check_types_fails_when_both_params_invalid(self):
        # Comprova que el mètode valida correctament el tipus dels dos paràmetres
        # Aquest test força l'execució completa de la condició lògica (or) a check_types()
    with self.assertRaises(TypeError):
        self.calc.add(None, None)

    def test_power_with_zero_base(self):
        # Comprova el càlcul de la potència amb base zero
        # Aquest test ajuda a garantir la cobertura completa de les línies del mètode power()
        self.assertEqual(0, self.calc.power(0, 3))    
        
if __name__ == "__main__":  # pragma: no cover
    unittest.main()
