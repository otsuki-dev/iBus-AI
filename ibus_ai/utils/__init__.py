"""
Módulo de Utilitários

Funções auxiliares para o pipeline de detecção.
"""

from .nms import (
    suprimir_nao_maximos,
    aplicar_nms_em_deteccoes,
    calcular_iou
)

__all__ = [
    'suprimir_nao_maximos',
    'aplicar_nms_em_deteccoes',
    'calcular_iou',
]
