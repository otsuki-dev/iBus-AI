"""
Predições em ROIs

Funções para fazer predições em regiões de interesse específicas.
"""

import numpy as np


def predizer_roi(roi, classificador, extrator_features):
    """
    Faz predição para uma única ROI.
    
    Args:
        roi (numpy.ndarray): Região de interesse
        classificador: Classificador treinado
        extrator_features: Função para extrair features
        
    Returns:
        dict: Resultado da predição com 'label' e 'confianca'
    """
    # Extrair features
    features = extrator_features(roi)
    features = features.reshape(1, -1)
    
    # Predizer
    label = classificador.predizer(features)[0]
    confianca = classificador.predizer_proba(features)[0]
    
    return {
        'label': int(label),
        'confianca': float(confianca),
        'e_pessoa': bool(label == 1)
    }


def predizer_multiplas_rois(rois, classificador, extrator_features, verbose=True):
    """
    Faz predições para múltiplas ROIs.
    
    Args:
        rois (list): Lista de regiões de interesse
        classificador: Classificador treinado
        extrator_features: Função para extrair features
        verbose (bool): Se True, exibe progresso
        
    Returns:
        list: Lista de resultados de predição
    """
    resultados = []
    
    for i, roi in enumerate(rois):
        try:
            resultado = predizer_roi(roi, classificador, extrator_features)
            resultados.append(resultado)
            
            if verbose and (i + 1) % 50 == 0:
                print(f"Processadas {i+1}/{len(rois)} ROIs")
                
        except Exception as e:
            if verbose:
                print(f"⚠ Erro ao processar ROI {i}: {str(e)}")
            resultados.append({
                'label': -1,
                'confianca': 0.0,
                'e_pessoa': False,
                'erro': str(e)
            })
    
    return resultados
