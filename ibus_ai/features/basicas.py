"""
Extração de Características Básicas

Funções para extrair características simples como bordas, cantos e histogramas.
"""

import numpy as np
import cv2
from skimage import color


def detectar_bordas_canny(imagem, sigma=1.0, limiar_baixo=50, limiar_alto=150):
    """
    Detecta bordas usando o algoritmo Canny.
    
    Args:
        imagem (numpy.ndarray): Imagem de entrada (RGB ou escala de cinza)
        sigma (float): Desvio padrão do filtro Gaussiano
        limiar_baixo (int): Limiar baixo para histerese
        limiar_alto (int): Limiar alto para histerese
        
    Returns:
        numpy.ndarray: Imagem de bordas binária
    """
    # Converter para escala de cinza se necessário
    if len(imagem.shape) == 3:
        imagem_gray = color.rgb2gray(imagem)
        imagem_gray = (imagem_gray * 255).astype(np.uint8)
    else:
        imagem_gray = imagem
    
    # Aplicar Canny
    bordas = cv2.Canny(imagem_gray, limiar_baixo, limiar_alto)
    
    return bordas


def detectar_cantos_harris(imagem, tamanho_bloco=2, tamanho_kernel=3, k=0.04, limiar=0.01):
    """
    Detecta cantos usando o detector de Harris.
    
    Args:
        imagem (numpy.ndarray): Imagem de entrada (RGB ou escala de cinza)
        tamanho_bloco (int): Tamanho da vizinhança considerada
        tamanho_kernel (int): Tamanho do kernel Sobel
        k (float): Parâmetro livre do detector de Harris
        limiar (float): Limiar para detecção de cantos (porcentagem do máximo)
        
    Returns:
        numpy.ndarray: Imagem com resposta de Harris
        numpy.ndarray: Coordenadas dos cantos detectados
    """
    # Converter para escala de cinza se necessário
    if len(imagem.shape) == 3:
        imagem_gray = color.rgb2gray(imagem)
        imagem_gray = (imagem_gray * 255).astype(np.uint8)
    else:
        imagem_gray = imagem.astype(np.uint8)
    
    # Detectar cantos
    dst = cv2.cornerHarris(imagem_gray, tamanho_bloco, tamanho_kernel, k)
    
    # Dilatar para marcar os cantos
    dst = cv2.dilate(dst, None)
    
    # Encontrar coordenadas dos cantos acima do limiar
    limiar_valor = limiar * dst.max()
    cantos = np.argwhere(dst > limiar_valor)
    
    return dst, cantos


def calcular_histograma_intensidade(imagem, num_bins=256):
    """
    Calcula o histograma de intensidades de uma imagem.
    
    Args:
        imagem (numpy.ndarray): Imagem de entrada (RGB ou escala de cinza)
        num_bins (int): Número de bins do histograma
        
    Returns:
        numpy.ndarray: Histograma normalizado
    """
    # Converter para escala de cinza se necessário
    if len(imagem.shape) == 3:
        imagem_gray = color.rgb2gray(imagem)
    else:
        imagem_gray = imagem
    
    # Calcular histograma
    hist, _ = np.histogram(imagem_gray.ravel(), bins=num_bins, range=(0, 1))
    
    # Normalizar
    hist = hist.astype(float) / hist.sum()
    
    return hist


def extrair_caracteristicas_basicas(imagem):
    """
    Extrai um conjunto de características básicas de uma imagem.
    
    Args:
        imagem (numpy.ndarray): Imagem de entrada
        
    Returns:
        dict: Dicionário com características extraídas:
            - 'num_bordas': Número de pixels de borda
            - 'num_cantos': Número de cantos detectados
            - 'intensidade_media': Intensidade média
            - 'intensidade_std': Desvio padrão da intensidade
            - 'histograma': Histograma de intensidades (16 bins)
    """
    # Converter para escala de cinza
    if len(imagem.shape) == 3:
        imagem_gray = color.rgb2gray(imagem)
    else:
        imagem_gray = imagem
    
    # Bordas
    bordas = detectar_bordas_canny(imagem)
    num_bordas = np.sum(bordas > 0)
    
    # Cantos
    _, cantos = detectar_cantos_harris(imagem)
    num_cantos = len(cantos)
    
    # Estatísticas de intensidade
    intensidade_media = np.mean(imagem_gray)
    intensidade_std = np.std(imagem_gray)
    
    # Histograma (16 bins para reduzir dimensionalidade)
    histograma = calcular_histograma_intensidade(imagem, num_bins=16)
    
    return {
        'num_bordas': num_bordas,
        'num_cantos': num_cantos,
        'intensidade_media': intensidade_media,
        'intensidade_std': intensidade_std,
        'histograma': histograma
    }
