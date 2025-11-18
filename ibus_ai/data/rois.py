"""
Gerenciamento de ROIs (Regions of Interest)

Funções para carregar, validar e manipular regiões de interesse.
"""

import json
import numpy as np


def carregar_rois(caminho_json):
    """
    Carrega ROIs de um arquivo JSON.
    
    Args:
        caminho_json (str): Caminho para o arquivo JSON com ROIs
        
    Returns:
        dict: Dicionário com ROIs carregadas
        
    Exemplo de formato JSON:
        {
            "imagem1.jpg": [
                {"x": 100, "y": 50, "w": 64, "h": 128, "label": "pessoa"},
                {"x": 200, "y": 60, "w": 64, "h": 128, "label": "pessoa"}
            ]
        }
    """
    with open(caminho_json, 'r') as f:
        rois = json.load(f)
    return rois


def validar_roi(roi, largura_img, altura_img):
    """
    Valida se uma ROI está dentro dos limites da imagem.
    
    Args:
        roi (dict): ROI com campos 'x', 'y', 'w', 'h'
        largura_img (int): Largura da imagem
        altura_img (int): Altura da imagem
        
    Returns:
        bool: True se a ROI é válida, False caso contrário
    """
    x, y, w, h = roi['x'], roi['y'], roi['w'], roi['h']
    
    # Verificar se está dentro dos limites
    if x < 0 or y < 0:
        return False
    if x + w > largura_img or y + h > altura_img:
        return False
    if w <= 0 or h <= 0:
        return False
    
    return True


def extrair_roi(imagem, roi):
    """
    Extrai uma região de interesse de uma imagem.
    
    Args:
        imagem (numpy.ndarray): Imagem como array NumPy
        roi (dict): ROI com campos 'x', 'y', 'w', 'h'
        
    Returns:
        numpy.ndarray: Região extraída da imagem
    """
    x, y, w, h = roi['x'], roi['y'], roi['w'], roi['h']
    return imagem[y:y+h, x:x+w]


def gerar_negativos_da_imagem(imagem, rois_positivas, tamanho_janela=(64, 128), num_negativos=10):
    """
    Gera exemplos negativos (não-pessoas) de áreas da imagem que não contêm ROIs positivas.
    
    Args:
        imagem (numpy.ndarray): Imagem completa
        rois_positivas (list): Lista de ROIs positivas (pessoas)
        tamanho_janela (tuple): Tamanho (largura, altura) das janelas negativas
        num_negativos (int): Número de exemplos negativos a gerar
        
    Returns:
        list: Lista de arrays NumPy com regiões negativas
    """
    altura_img, largura_img = imagem.shape[:2]
    largura_janela, altura_janela = tamanho_janela
    
    negativos = []
    tentativas = 0
    max_tentativas = num_negativos * 10  # Evitar loop infinito
    
    while len(negativos) < num_negativos and tentativas < max_tentativas:
        tentativas += 1
        
        # Gerar posição aleatória
        x = np.random.randint(0, max(1, largura_img - largura_janela))
        y = np.random.randint(0, max(1, altura_img - altura_janela))
        
        # Verificar se não sobrepõe com ROIs positivas
        sobrepoe = False
        for roi in rois_positivas:
            if _rois_sobrepoem(
                (x, y, largura_janela, altura_janela),
                (roi['x'], roi['y'], roi['w'], roi['h'])
            ):
                sobrepoe = True
                break
        
        if not sobrepoe:
            # Extrair região negativa
            regiao = imagem[y:y+altura_janela, x:x+largura_janela]
            if regiao.shape[:2] == (altura_janela, largura_janela):
                negativos.append(regiao)
    
    return negativos


def _rois_sobrepoem(roi1, roi2, threshold=0.3):
    """
    Verifica se duas ROIs se sobrepõem significativamente.
    
    Args:
        roi1 (tuple): (x, y, w, h) da primeira ROI
        roi2 (tuple): (x, y, w, h) da segunda ROI
        threshold (float): Limiar de sobreposição (IoU)
        
    Returns:
        bool: True se há sobreposição significativa
    """
    x1, y1, w1, h1 = roi1
    x2, y2, w2, h2 = roi2
    
    # Calcular interseção
    x_esq = max(x1, x2)
    y_topo = max(y1, y2)
    x_dir = min(x1 + w1, x2 + w2)
    y_baixo = min(y1 + h1, y2 + h2)
    
    if x_dir < x_esq or y_baixo < y_topo:
        return False
    
    area_intersecao = (x_dir - x_esq) * (y_baixo - y_topo)
    area_roi1 = w1 * h1
    area_roi2 = w2 * h2
    area_uniao = area_roi1 + area_roi2 - area_intersecao
    
    iou = area_intersecao / area_uniao if area_uniao > 0 else 0
    
    return iou > threshold
