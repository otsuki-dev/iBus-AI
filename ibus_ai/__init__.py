"""
iBus-AI: Sistema de Detecção de Pessoas em Ônibus

Um sistema completo de visão computacional para detectar e contar pessoas
em ambientes internos de ônibus usando técnicas clássicas (HOG + SVM).

Módulos:
    - data: Pré-processamento de imagens e gerenciamento de ROIs
    - features: Extração de características (HOG, bordas, cantos)
    - models: Modelos de classificação (SVM)
    - infer: Pipeline de detecção e predição
    - utils: Funções utilitárias (NMS, etc)
"""

__version__ = "1.0.0"
__author__ = "iBus-AI Team"

# Importações convenientes
from .data.preprocess import carregar_e_preprocessar_imagem, criar_imagem_dummy
from .data.rois import carregar_rois, gerar_negativos_da_imagem
from .features.hog import extrair_hog, extrair_hog_de_rois
from .models.svm import ClassificadorPessoas, treinar_classificador_do_zero
from .infer.detect import sliding_window_deteccao
from .utils.nms import suprimir_nao_maximos, aplicar_nms_em_deteccoes

__all__ = [
    # Data
    'carregar_e_preprocessar_imagem',
    'criar_imagem_dummy',
    'carregar_rois',
    'gerar_negativos_da_imagem',
    # Features
    'extrair_hog',
    'extrair_hog_de_rois',
    # Models
    'ClassificadorPessoas',
    'treinar_classificador_do_zero',
    # Infer
    'sliding_window_deteccao',
    # Utils
    'suprimir_nao_maximos',
    'aplicar_nms_em_deteccoes',
]
