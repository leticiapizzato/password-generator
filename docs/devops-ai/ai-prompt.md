Atue como engenheiro DevOps/QA especialista em Python e CI/CD.

Contexto: o job de testes de um pipeline falhou. Projeto: CLI de geracao de
senhas (main.py -> cli_argparse.py -> generator.py), testada com pytest.
Regra documentada (RF04): --length aceita 8..32, limites INCLUSIVOS.

Testes que falharam:
FAILED tests/integration/test_cli_integration.py::test_length_flag_propagates_through_all_layers[32]
FAILED tests/integration/test_cli_integration.py::test_default_run_contains_all_four_classes
FAILED tests/integration/test_cli_integration.py::test_disabling_one_class_removes_it_end_to_end[--no-upper-ABCDEFGHIJKLMNOPQRSTUVWXYZ]
FAILED tests/integration/test_cli_integration.py::test_disabling_one_class_removes_it_end_to_end[--no-lower-abcdefghijklmnopqrstuvwxyz]
FAILED tests/integration/test_cli_integration.py::test_disabling_one_class_removes_it_end_to_end[--no-number-0123456789]
FAILED tests/integration/test_cli_integration.py::test_disabling_one_class_removes_it_end_to_end[--no-wildcards-!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~]
FAILED tests/integration/test_cli_integration_edge.py::test_inclusive_bounds_are_accepted[32]
FAILED tests/test_generator.py::test_generate_password_accepts_inclusive_bounds[32]
FAILED tests/test_generator.py::test_disabled_class_is_absent_from_password
FAILED tests/test_generator.py::test_special_characters_belong_to_expected_set

Trecho relevante do log:
```
ios selecionados.
    
        Args:
            length: Quantidade de caracteres da senha.
            upper: Indica se letras maiusculas devem ser consideradas.
            lower: Indica se letras minusculas devem ser consideradas.
            number: Indica se numeros devem ser considerados.
            wildcards: Indica se caracteres especiais devem ser considerados.
    
        Returns:
            Senha gerada aleatoriamente.
    
        Raises:
            TypeError: Se o tipo de length nao for inteiro.
            ValueError: Se o tamanho estiver fora da faixa permitida.
            ValueError: Se nenhuma classe de caractere for selecionada.
        """
        if not isinstance(length, int):
            raise TypeError("O parametro length deve ser do tipo inteiro.")
    
        if not MIN_LENGTH <= length < MAX_LENGTH:
>           raise ValueError(
                f"O tamanho da senha deve estar entre {MIN_LENGTH} e {MAX_LENGTH}."
            )
E           ValueError: O tamanho da senha deve estar entre 8 e 32.

src\generator.py:42: ValueError
_________________ test_disabled_class_is_absent_from_password _________________

    def test_disabled_class_is_absent_from_password() -> None:
        """Uma classe desligada nao deve aparecer na senha gerada."""
>       password=***
            length=32,
            lower=False,
            upper=True,
            number=True,
            wildcards=False,
        )

tests\test_generator.py:190: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

length = 32, upper = True, lower = False, number = True, wildcards = False

    def generate_password(
        length: int = 16,
        upper: bool = True,
        lower: bool = True,
        number: bool = True,
        wildcards: bool = True,
    ) -> str:
        """Gera uma senha segura com base nos criterios selecionados.
    
        Args:
            length: Quantidade de caracteres da senha.
            upper: Indica se letras maiusculas devem ser consideradas.
            lower: Indica se letras minusculas devem ser consideradas.
            number: Indica se numeros devem ser considerados.
            wildcards: Indica se caracteres especiais devem ser considerados.
    
        Returns:
            Senha gerada aleatoriamente.
    
        Raises:
            TypeError: Se o tipo de length nao for inteiro.
            ValueError: Se o tamanho estiver fora da faixa permitida.
            ValueError: Se nenhuma classe de caractere for selecionada.
        """
        if not isinstance(length, int):
            raise TypeError("O parametro length deve ser do tipo inteiro.")
    
        if not MIN_LENGTH <= length < MAX_LENGTH:
>           raise ValueError(
                f"O tamanho da senha deve estar entre {MIN_LENGTH} e {MAX_LENGTH}."
            )
E           ValueError: O tamanho da senha deve estar entre 8 e 32.

src\generator.py:42: ValueError
_______________ test_special_characters_belong_to_expected_set ________________

    def test_special_characters_belong_to_expected_set() -> None:
        """Os especiais usados devem ser exatamente os de string.punctuation."""
>       password=***
            length=32,
            lower=False,
            upper=False,
            number=False,
            wildcards=True,
        )

tests\test_generator.py:206: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

length = 32, upper = False, lower = False, number = False, wildcards = True

    def generate_password(
        length: int = 16,
        upper: bool = True,
        lower: bool = True,
        number: bool = True,
        wildcards: bool = True,
    ) -> str:
        """Gera uma senha segura com base nos criterios selecionados.
    
        Args:
            length: Quantidade de caracteres da senha.
            upper: Indica se letras maiusculas devem ser consideradas.
            lower: Indica se letras minusculas devem ser consideradas.
            number: Indica se numeros devem ser considerados.
            wildcards: Indica se caracteres especiais devem ser considerados.
    
        Returns:
            Senha gerada aleatoriamente.
    
        Raises:
            TypeError: Se o tipo de length nao for inteiro.
            ValueError: Se o tamanho estiver fora da faixa permitida.
            ValueError: Se nenhuma classe de caractere for selecionada.
        """
        if not isinstance(length, int):
            raise TypeError("O parametro length deve ser do tipo inteiro.")
    
        if not MIN_LENGTH <= length < MAX_LENGTH:
>           raise ValueError(
                f"O tamanho da senha deve estar entre {MIN_LENGTH} e {MAX_LENGTH}."
            )
E           ValueError: O tamanho da senha deve estar entre 8 e 32.

src\generator.py:42: ValueError
=========================== short test summary info ===========================
FAILED tests/integration/test_cli_integration.py::test_length_flag_propagates_through_all_layers[32]
FAILED tests/integration/test_cli_integration.py::test_default_run_contains_all_four_classes
FAILED tests/integration/test_cli_integration.py::test_disabling_one_class_removes_it_end_to_end[--no-upper-ABCDEFGHIJKLMNOPQRSTUVWXYZ]
FAILED tests/integration/test_cli_integration.py::test_disabling_one_class_removes_it_end_to_end[--no-lower-abcdefghijklmnopqrstuvwxyz]
FAILED tests/integration/test_cli_integration.py::test_disabling_one_class_removes_it_end_to_end[--no-number-0123456789]
FAILED tests/integration/test_cli_integration.py::test_disabling_one_class_removes_it_end_to_end[--no-wildcards-!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~]
FAILED tests/integration/test_cli_integration_edge.py::test_inclusive_bounds_are_accepted[32]
FAILED tests/test_generator.py::test_generate_password_accepts_inclusive_bounds[32]
FAILED tests/test_generator.py::test_disabled_class_is_absent_from_password
FAILED tests/test_generator.py::test_special_characters_belong_to_expected_set
10 failed, 48 passed in 12.33s

```

Codigo-fonte suspeito (src/generator.py):
```python
ï»¿"""Core de geracao de senhas seguras."""

from __future__ import annotations

import secrets
import string

#: Limites de tamanho da senha. Fonte unica de verdade: a CLI importa estas
#: constantes em vez de repetir os valores (evita divergencia entre camadas).
MIN_LENGTH = 8
MAX_LENGTH = 32


def generate_password(
    length: int = 16,
    upper: bool = True,
    lower: bool = True,
    number: bool = True,
    wildcards: bool = True,
) -> str:
    """Gera uma senha segura com base nos criterios selecionados.

    Args:
        length: Quantidade de caracteres da senha.
        upper: Indica se letras maiusculas devem ser consideradas.
        lower: Indica se letras minusculas devem ser consideradas.
        number: Indica se numeros devem ser considerados.
        wildcards: Indica se caracteres especiais devem ser considerados.

    Returns:
        Senha gerada aleatoriamente.

    Raises:
        TypeError: Se o tipo de length nao for inteiro.
        ValueError: Se o tamanho estiver fora da faixa permitida.
        ValueError: Se nenhuma classe de caractere for selecionada.
    """
    if not isinstance(length, int):
        raise TypeError("O parametro length deve ser do tipo inteiro.")

    if not MIN_LENGTH <= length < MAX_LENGTH:
        raise ValueError(
            f"O tamanho da senha deve estar entre {MIN_LENGTH} e {MAX_LENGTH}."
        )

    selected_sets: list[str] = []
    if upper:
        selected_sets.append(string.ascii_uppercase)
    if lower:
        selected_sets.append(string.ascii_lowercase)
    if number:
        selected_sets.append(string.digits)
    if wildcards:
        selected_sets.append(string.punctuation)

    if not selected_sets:
        raise ValueError("Selecione ao menos uma classe de caractere.")

    # Nao ha checagem de "tamanho < numero de classes": com MIN_LENGTH = 8 e no
    # maximo 4 classes, a condicao e sempre falsa. A validacao existia e era
    # codigo morto (RF10). Ver requisitos/analise-elicitacao.md secao 7.1.

    # Garante ao menos um caractere de cada classe selecionada.
    password_chars = [secrets.choice(chars) for chars in selected_sets]

    alphabet = "".join(selected_sets)
    remaining = length - len(password_chars)
    password_chars.extend(secrets.choice(alphabet) for _ in range(remaining))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)



```

Tarefa (nao altere nada, apenas diagnostique):
1. Identifique a causa raiz e a linha responsavel.
2. Classifique como defeito, erro ou falha.
3. Sugira a correcao minima.
4. Aponte o que precisa ser validado por um humano antes de aplicar.
