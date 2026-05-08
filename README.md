# Calculadora — TDD: Red · Green · Refactor

Ejercicio práctico de **Desarrollo Guiado por Pruebas** (Test-Driven Development)
aplicado a una calculadora con operaciones aritméticas básicas en Python.

---

## Tabla de contenidos

1. [¿Qué es TDD?](#1-qué-es-tdd)
2. [El ciclo Red · Green · Refactor](#2-el-ciclo-red--green--refactor)
3. [Estructura del proyecto](#3-estructura-del-proyecto)
4. [Cómo ejecutar las pruebas](#4-cómo-ejecutar-las-pruebas)
5. [Fase 🔴 RED — Escribir el test primero](#5-fase--red--escribir-el-test-primero)
6. [Fase 🟢 GREEN — Implementación mínima](#6-fase--green--implementación-mínima)
7. [Fase 🔵 REFACTOR — Mejorar sin romper](#7-fase--refactor--mejorar-sin-romper)
8. [Tabla de evolución por iteración](#8-tabla-de-evolución-por-iteración)
9. [El bug que el test atrapó](#9-el-bug-que-el-test-atrapó)
10. [Métodos de aserción utilizados](#10-métodos-de-aserción-utilizados)
11. [Conclusiones](#11-conclusiones)

---

## 1. ¿Qué es TDD?

TDD (**Test-Driven Development**) es una metodología de desarrollo de software en la que
**las pruebas se escriben antes que el código de producción**.

El objetivo no es solo probar que el código funciona, sino usar las pruebas como
**guía de diseño**: cada test describe un comportamiento que el sistema debe cumplir,
y el código existe únicamente para satisfacer esos tests.

### Regla de oro del TDD

> *"No escribas código de producción a menos que sea para hacer pasar un test que está fallando."*
> — Kent Beck, creador de TDD

---

## 2. El ciclo Red · Green · Refactor

El TDD se estructura en un ciclo de tres fases que se repite continuamente:

```
        ┌─────────────────────────────────────────────────────┐
        │                                                     │
        ▼                                                     │
  ┌───────────┐      falla      ┌───────────┐    pasa    ┌───────────┐
  │  🔴 RED   │ ──────────────► │ 🟢 GREEN  │ ──────────►│🔵REFACTOR │
  │           │                 │           │            │           │
  │  Escribe  │                 │  Escribe  │            │  Mejora   │
  │  el test  │                 │  el mínimo│            │  el código│
  │  primero  │                 │  código   │            │  sin      │
  │           │                 │  posible  │            │  romper   │
  └───────────┘                 └───────────┘            └───────────┘
```

| Fase | Color | Pregunta que responde |
|---|---|---|
| **RED** | 🔴 | ¿Qué comportamiento necesito? |
| **GREEN** | 🟢 | ¿Cuál es la solución más simple posible? |
| **REFACTOR** | 🔵 | ¿Cómo mejoro el código sin cambiar su comportamiento? |

---

## 3. Estructura del proyecto

```
Calculadora/
│
├── calculadora.py        ← Código de producción (se escribe en GREEN y REFACTOR)
├── test_calculadora.py   ← Pruebas unitarias    (se escribe primero, en RED)
└── README.md             ← Este documento
```

### Flujo de dependencia

```
test_calculadora.py
        │
        │  importa
        ▼
calculadora.py  →  class Calculadora
                        ├── sumar()
                        ├── restar()
                        ├── multiplicar()
                        ├── dividir()
                        └── _validar()   ← añadido en REFACTOR
```

---

## 4. Cómo ejecutar las pruebas

Desde la carpeta `Calculadora/`, ejecuta:

```
py -m unittest test_calculadora -v
```

La bandera `-v` (verbose) muestra el nombre de cada test y su resultado individual.

### Interpretación de la salida

```
test_suma_dos_positivos ... ok        ← Test pasó   ✅
test_dividir_por_cero   ... ERROR     ← Excepción no esperada ❌
test_suma_dos_positivos ... FAIL      ← Aserción falsa ❌

----------------------------------------------------------------------
Ran 11 tests in 0.005s

OK          ← Todos pasaron ✅
FAILED (errors=3)   ← Hay fallos ❌
```

---

## 5. Fase 🔴 RED — Escribir el test primero

### ¿Qué se hace en esta fase?

Se escribe el archivo `test_calculadora.py` con **todos los casos de prueba**
antes de que exista ninguna implementación. En este momento el código falla,
y eso es **exactamente lo correcto**.

### ¿Por qué escribir el test antes?

- Obliga a pensar en el **diseño y la interfaz** antes que en la implementación.
- Documenta el comportamiento esperado de forma ejecutable.
- Garantiza que el test realmente detecta errores (si no falla en rojo, no vale).

### Archivo: `test_calculadora.py`

```python
import unittest
from calculadora import Calculadora   # ← calculadora.py NO existe aún

class TestCalculadora(unittest.TestCase):

    def setUp(self):
        # setUp() se ejecuta antes de CADA test.
        # Garantiza que cada prueba parte de un estado limpio.
        self.calc = Calculadora()

    # ── SUMA ──────────────────────────────────────────────────
    def test_suma_dos_positivos(self):
        self.assertEqual(self.calc.sumar(3, 4), 7)

    def test_suma_con_negativo(self):
        self.assertEqual(self.calc.sumar(-2, 5), 3)

    def test_suma_cero(self):
        self.assertEqual(self.calc.sumar(0, 9), 9)

    # ── RESTA ─────────────────────────────────────────────────
    def test_resta_positivos(self):
        self.assertEqual(self.calc.restar(10, 4), 6)

    def test_resta_resultado_negativo(self):
        self.assertEqual(self.calc.restar(3, 8), -5)

    # ── MULTIPLICACIÓN ────────────────────────────────────────
    def test_multiplicar_positivos(self):
        self.assertEqual(self.calc.multiplicar(3, 5), 15)

    def test_multiplicar_por_cero(self):
        self.assertEqual(self.calc.multiplicar(99, 0), 0)

    def test_multiplicar_negativos(self):
        self.assertEqual(self.calc.multiplicar(-3, -4), 12)

    # ── DIVISIÓN ──────────────────────────────────────────────
    def test_dividir_exacta(self):
        self.assertEqual(self.calc.dividir(10, 2), 5)

    def test_dividir_resultado_decimal(self):
        self.assertAlmostEqual(self.calc.dividir(1, 3), 0.3333, places=4)

    def test_dividir_por_cero_lanza_error(self):          # ← caso borde crítico
        with self.assertRaises(ValueError) as ctx:
            self.calc.dividir(10, 0)
        self.assertIn("cero", str(ctx.exception).lower())
```

### Salida en terminal — Estado ROJO

Al ejecutar `py -m unittest test_calculadora -v` sin haber creado `calculadora.py`:

```
ERROR: test_calculadora (unittest.loader._FailedTest.test_calculadora)
----------------------------------------------------------------------
ModuleNotFoundError: No module named 'calculadora'

Ran 1 test in 0.001s
FAILED (errors=1)
```

> **El error `ModuleNotFoundError` confirma la fase ROJA.**
> El test intenta importar algo que no existe. El ciclo puede avanzar.

---

## 6. Fase 🟢 GREEN — Implementación mínima

### ¿Qué se hace en esta fase?

Se escribe **el código más simple posible** para que los tests pasen.
Sin optimizaciones, sin validaciones extra, sin documentación todavía.
La única pregunta es: *¿qué mínimo hace que el test deje de fallar?*

### Evolución iterativa (método a método)

En TDD, lo ideal es avanzar en pasos pequeños: añadir un método, correr los tests,
verificar progreso, continuar.

---

#### Iteración 1 — Clase vacía

```python
class Calculadora:
    pass
```

```
Ran 11 tests in 0.017s
FAILED (errors=11)   → AttributeError: 'Calculadora' object has no attribute 'sumar'
```

La clase existe pero no tiene métodos. El error cambió:
ya no es un problema de módulo sino de atributos faltantes. Progreso.

---

#### Iteración 2 — Se añade `sumar`

```python
class Calculadora:
    def sumar(self, a, b):
        return a + b
```

```
test_suma_cero           ... ok   ✅
test_suma_con_negativo   ... ok   ✅
test_suma_dos_positivos  ... ok   ✅
...
Ran 11 tests    FAILED (errors=8)
```

3 tests pasan, 8 siguen fallando. El contador verde empieza a subir.

---

#### Iteración 3 — Se añade `restar`

```python
    def restar(self, a, b):
        return a - b
```

```
test_resta_positivos         ... ok   ✅
test_resta_resultado_negativo ... ok   ✅
Ran 11 tests    FAILED (errors=6)
```

5 tests pasan, 6 fallan.

---

#### Iteración 4 — Se añade `multiplicar`

```python
    def multiplicar(self, a, b):
        return a * b
```

```
test_multiplicar_negativos ... ok   ✅
test_multiplicar_por_cero  ... ok   ✅
test_multiplicar_positivos ... ok   ✅
Ran 11 tests    FAILED (errors=3)
```

8 tests pasan, 3 fallan. Solo queda la división.

---

#### Iteración 5a — Se añade `dividir` SIN protección de cero (bug intencional)

```python
    def dividir(self, a, b):
        return a / b    # ← sin guard de cero
```

```
test_dividir_exacta          ... ok    ✅
test_dividir_resultado_decimal ... ok  ✅
test_dividir_por_cero_lanza_error ... ERROR  ❌

ZeroDivisionError: division by zero
Ran 11 tests    FAILED (errors=1)
```

> **El test detecta el bug antes de que llegue a producción.**
> Python lanza `ZeroDivisionError`, pero el test exige `ValueError`.
> Sin ese test, este bug habría pasado desapercibido.

---

#### Iteración 5b — Se corrige `dividir` con el guard correcto

```python
    def dividir(self, a, b):
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b
```

```
Ran 11 tests in 0.005s
OK   ✅✅✅✅✅✅✅✅✅✅✅
```

**11 de 11 tests en verde. Fase GREEN completada.**

### Código al final de la fase GREEN

```python
class Calculadora:

    def sumar(self, a, b):
        return a + b

    def restar(self, a, b):
        return a - b

    def multiplicar(self, a, b):
        return a * b

    def dividir(self, a, b):
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b
```

Es funcional pero sin documentación, sin type hints y con lógica de validación
duplicada en cada método. Es el momento ideal para el refactor.

---

## 7. Fase 🔵 REFACTOR — Mejorar sin romper

### ¿Qué se hace en esta fase?

Se mejora la **calidad interna** del código sin cambiar su comportamiento externo.
Los tests **no se modifican en absoluto** — son la red de seguridad que garantiza
que la refactorización no introduce regresiones.

### ¿Qué se mejoró y por qué?

| Mejora aplicada | Problema que resuelve |
|---|---|
| `_validar()` como método privado | Elimina duplicación: la validación estaba implícita en cada método |
| `type hints` (`Numero`, `float`) | Documenta los tipos esperados de forma ejecutable |
| `docstrings` en cada método | Permite generar documentación y ayuda al IDE |
| `__repr__` | Representación útil al hacer debugging en consola |
| Alias `Numero = Union[int, float]` | Evita repetir el tipo en cada firma |

### Código al final de la fase REFACTOR

```python
from typing import Union

Numero = Union[int, float]          # ← alias de tipo para reutilizar


class Calculadora:
    """Calculadora con operaciones aritméticas básicas."""

    def _validar(self, *args: Numero) -> None:
        """
        Verifica que todos los argumentos sean int o float.
        Lanza TypeError si alguno no lo es.
        Método privado reutilizado por todas las operaciones.
        """
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
        Raises ValueError si b es igual a cero.
        """
        self._validar(a, b)
        if b == 0:
            raise ValueError(
                "No se puede dividir por cero. "
                "El divisor debe ser distinto de cero."
            )
        return a / b

    def __repr__(self) -> str:
        return "Calculadora()"
```

### Salida en terminal — Post-refactor

```
test_dividir_exacta                ... ok
test_dividir_por_cero_lanza_error  ... ok
test_dividir_resultado_decimal     ... ok
test_multiplicar_negativos         ... ok
test_multiplicar_por_cero          ... ok
test_multiplicar_positivos         ... ok
test_resta_positivos               ... ok
test_resta_resultado_negativo      ... ok
test_suma_cero                     ... ok
test_suma_con_negativo             ... ok
test_suma_dos_positivos            ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.004s

OK
```

> **11/11 siguen en verde.** El refactor fue exitoso: el código mejoró y ningún
> comportamiento se rompió. Los tests actuaron como red de seguridad.

---

## 8. Tabla de evolución por iteración

La siguiente tabla muestra cómo el contador de tests verdes fue subiendo a medida
que se añadía cada método durante la fase GREEN.

| Iteración | Código añadido | Tests ✅ | Tests ❌ | Estado |
|:---------:|---|:---:|:---:|:---:|
| 0 | Sin `calculadora.py` | 0 | — | 🔴 `ModuleNotFoundError` |
| 1 | `class Calculadora: pass` | 0 | 11 | 🔴 `AttributeError` x11 |
| 2 | `+ sumar()` | 3 | 8 | 🔴 parcial |
| 3 | `+ restar()` | 5 | 6 | 🔴 parcial |
| 4 | `+ multiplicar()` | 8 | 3 | 🔴 parcial |
| 5a | `+ dividir()` sin guard | 10 | 1 | 🔴 bug detectado |
| 5b | `+ dividir()` con guard | **11** | **0** | 🟢 **GREEN** |
| 6 | Refactor completo | **11** | **0** | 🔵 **REFACTOR** |

---

## 9. El bug que el test atrapó

Este es el momento más instructivo del ejercicio. En la **iteración 5a**,
se implementó `dividir` de forma incompleta:

```python
# Implementación incorrecta (sin guard)
def dividir(self, a, b):
    return a / b
```

Al ejecutar los tests, el test `test_dividir_por_cero_lanza_error` falló así:

```
ERROR: test_dividir_por_cero_lanza_error
----------------------------------------------------------------------
ZeroDivisionError: division by zero
```

El test esperaba un `ValueError` con la palabra "cero" en el mensaje.
Python lanzó en su lugar un `ZeroDivisionError` genérico sin mensaje útil.

Sin el test, este bug habría llegado a producción silenciosamente,
causando una excepción genérica e incomprensible para el usuario final.

**Con el test, fue detectado y corregido en segundos.**

---

## 10. Métodos de aserción utilizados

| Método | ¿Qué verifica? | Ejemplo en el ejercicio |
|---|---|---|
| `assertEqual(a, b)` | Que `a == b` exactamente | `sumar(3, 4) == 7` |
| `assertAlmostEqual(a, b, places=n)` | Que `a ≈ b` con `n` decimales de tolerancia | `dividir(1, 3) ≈ 0.3333` |
| `assertRaises(Error)` | Que el bloque lanza la excepción indicada | `dividir(10, 0)` lanza `ValueError` |
| `assertIn(x, contenedor)` | Que `x` está dentro de `contenedor` | `"cero"` aparece en el mensaje de error |

---

## 11. Conclusiones

### ¿Qué se gana con TDD?

- **Diseño más limpio:** pensar el test primero obliga a diseñar interfaces simples y claras.
- **Confianza para cambiar código:** el refactor fue posible sin miedo porque los tests actúan como red de seguridad.
- **Documentación viva:** cada test describe un comportamiento del sistema de forma legible y ejecutable.
- **Detección temprana de bugs:** el bug de `ZeroDivisionError` fue atrapado antes de escribir el código correcto.

### Comparación: Con TDD vs Sin TDD

| Aspecto | Sin TDD | Con TDD |
|---|---|---|
| ¿Cuándo se detectan bugs? | En producción | Antes de terminar el método |
| ¿Qué tan seguro es refactorizar? | Arriesgado | Seguro (los tests verifican) |
| ¿Cómo se documenta el comportamiento? | Con comentarios (se desactualizan) | Con tests (siempre ejecutables) |
| ¿Cuándo se piensa en el diseño? | Después de escribir | Antes de escribir |

### El ciclo nunca termina

```
  Nuevo requisito
        │
        ▼
  🔴 Escribir test  →  🟢 Mínima implementación  →  🔵 Refactor
        ▲                                                  │
        └──────────────────────────────────────────────────┘
                     Siguiente iteración
```

Cada nueva funcionalidad reinicia el ciclo, siempre empezando por el test.

---

*Ejercicio desarrollado con Python 3.13 · unittest (biblioteca estándar)*
