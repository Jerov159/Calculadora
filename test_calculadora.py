import unittest

from calculadora import Calculadora  # calculadora.py NO existe aún


class TestCalculadora(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    # --- RONDA 1: SUMA ---
    def test_suma_dos_positivos(self):
        self.assertEqual(self.calc.sumar(3, 4), 7)

    def test_suma_con_negativo(self):
        self.assertEqual(self.calc.sumar(-2, 5), 3)

    def test_suma_cero(self):
        self.assertEqual(self.calc.sumar(0, 9), 9)

    # --- RONDA 2: RESTA ---
    def test_resta_positivos(self):
        self.assertEqual(self.calc.restar(10, 4), 6)

    def test_resta_resultado_negativo(self):
        self.assertEqual(self.calc.restar(3, 8), -5)

    # --- RONDA 3: MULTIPLICACIÓN ---
    def test_multiplicar_positivos(self):
        self.assertEqual(self.calc.multiplicar(3, 5), 15)

    def test_multiplicar_por_cero(self):
        self.assertEqual(self.calc.multiplicar(99, 0), 0)

    def test_multiplicar_negativos(self):
        self.assertEqual(self.calc.multiplicar(-3, -4), 12)

    # --- RONDA 4: DIVISIÓN ---
    def test_dividir_exacta(self):
        self.assertEqual(self.calc.dividir(10, 2), 5)

    def test_dividir_resultado_decimal(self):
        self.assertAlmostEqual(self.calc.dividir(1, 3), 0.3333, places=4)

    def test_dividir_por_cero_lanza_error(self):
        with self.assertRaises(ValueError) as ctx:
            self.calc.dividir(10, 0)
        self.assertIn("cero", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
