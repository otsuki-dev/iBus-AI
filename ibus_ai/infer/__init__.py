"""
Módulo de Inferência

Funções para detectar pessoas em imagens usando o modelo treinado.
"""

from .detect import (
    sliding_window_deteccao,
    extrair_caixas_de_deteccoes,
    detectar_pessoas_multiescala
)

from .predict import (
    predizer_roi,
    predizer_multiplas_rois
)

__all__ = [
    'sliding_window_deteccao',
    'extrair_caixas_de_deteccoes',
    'detectar_pessoas_multiescala',
    'predizer_roi',
    'predizer_multiplas_rois',
]
