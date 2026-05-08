from typing import Union

Numero = Union[int, float]


class Calculadora:
    """Calculadora con operaciones aritméticas básicas."""

    def _validar(self, *args: Numero) -> None:
        """Lanza TypeError si algún argumento no es int ni float."""
        for valor in args:
            if not isinstance(valor, (int, float)):
                raise TypeError(
                    f"Se esperaba un número, se recibió: {type(valor).__name__!r}"
                )

    def sumar(self, a: Numero, b: Numero) -> Numero:
        """Retorna a + b."""
        self._validar(a, b)
        return a + b

    def restar(self, a: Numero, b: Numero) -> Numero:
        """Retorna a - b."""
        self._validar(a, b)
        return a - b

    def multiplicar(self, a: Numero, b: Numero) -> Numero:
        """Retorna a * b."""
        self._validar(a, b)
        return a * b

    def dividir(self, a: Numero, b: Numero) -> float:
        """
        Retorna a / b.
        Raises ValueError si b == 0.
        """
        self._validar(a, b)
        if b == 0:
            raise ValueError(
                "No se puede dividir por cero. El divisor debe ser distinto de cero."
            )
        return a / b

    def __repr__(self) -> str:
        return "Calculadora()"
