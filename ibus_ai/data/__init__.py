"""
Módulo de Dados

Funções para carregar, pré-processar imagens e gerenciar ROIs.
"""

from .preprocess import (
    carregar_e_preprocessar_imagem,
    criar_imagem_dummy,
    carregar_multiplas_imagens
)

from .rois import (
    carregar_rois,
    gerar_negativos_da_imagem,
    extrair_roi,
    validar_roi
)

__all__ = [
    'carregar_e_preprocessar_imagem',
    'criar_imagem_dummy',
    'carregar_multiplas_imagens',
    'carregar_rois',
    'gerar_negativos_da_imagem',
    'extrair_roi',
    'validar_roi',
]
