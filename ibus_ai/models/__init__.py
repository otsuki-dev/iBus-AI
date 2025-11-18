"""
Módulo de Modelos de Classificação

Implementação de classificadores para detecção de pessoas.
"""

from .svm import (
    ClassificadorPessoas,
    treinar_classificador_do_zero,
    avaliar_classificador
)

__all__ = [
    'ClassificadorPessoas',
    'treinar_classificador_do_zero',
    'avaliar_classificador',
]
