"""
Módulo de Extração de Características

Funções para extrair features de imagens (HOG, bordas, cantos, histogramas).
"""

from .hog import (
    extrair_hog,
    extrair_hog_de_rois,
    padronizar_caracteristicas
)

from .basicas import (
    detectar_bordas_canny,
    detectar_cantos_harris,
    calcular_histograma_intensidade,
    extrair_caracteristicas_basicas
)

__all__ = [
    # HOG
    'extrair_hog',
    'extrair_hog_de_rois',
    'padronizar_caracteristicas',
    # Básicas
    'detectar_bordas_canny',
    'detectar_cantos_harris',
    'calcular_histograma_intensidade',
    'extrair_caracteristicas_basicas',
]
