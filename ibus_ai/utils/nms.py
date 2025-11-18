""""""

Non-Maximum Suppression (NMS)Módulo de Supressão Não-Máxima (NMS)

Função para consolidar detecções sobrepostas

Implementação de NMS para eliminar detecções redundantes/sobrepostas."""

"""

import numpy as np

import numpy as np



def suprimir_nao_maximos(caixas, limiar_sobreposicao=0.3):

def calcular_iou(caixa1, caixa2):    """

    """    Aplica Supressão Não-Máxima (Non-Maximum Suppression - NMS) nas detecções.

    Calcula IoU (Intersection over Union) entre duas caixas.    

        NMS remove detecções redundantes que se sobrepõem significativamente,

    Args:    mantendo apenas a detecção com maior confiança em cada região.

        caixa1 (tuple): (x, y, w, h) da primeira caixa    

        caixa2 (tuple): (x, y, w, h) da segunda caixa    Args:

                caixas: Array numpy (N x 4) com formato [x, y, w, h]

    Returns:        limiar_sobreposicao: Limiar de sobreposição IoU (0-1)

        float: Valor de IoU entre 0 e 1                            Valor menor = mais agressivo na remoção

    """                            

    x1, y1, w1, h1 = caixa1    Returns:

    x2, y2, w2, h2 = caixa2        Array numpy de caixas filtradas no formato [x, y, w, h]

        """

    # Calcular coordenadas da interseção    if len(caixas) == 0:

    x_esq = max(x1, x2)        return np.array([])

    y_topo = max(y1, y2)    

    x_dir = min(x1 + w1, x2 + w2)    # Converter para float se necessário

    y_baixo = min(y1 + h1, y2 + h2)    if caixas.dtype.kind == "i":

            caixas = caixas.astype("float")

    # Se não há interseção    

    if x_dir < x_esq or y_baixo < y_topo:    # Inicializar lista de índices escolhidos

        return 0.0    escolhidos = []

        

    # Calcular áreas    # Obter coordenadas das caixas delimitadoras

    area_intersecao = (x_dir - x_esq) * (y_baixo - y_topo)    x1 = caixas[:, 0]

    area_caixa1 = w1 * h1    y1 = caixas[:, 1]

    area_caixa2 = w2 * h2    x2 = caixas[:, 0] + caixas[:, 2]

    area_uniao = area_caixa1 + area_caixa2 - area_intersecao    y2 = caixas[:, 1] + caixas[:, 3]

        

    # Calcular IoU    # Calcular área das caixas delimitadoras e ordenar pelas coordenadas y inferiores-direitas

    iou = area_intersecao / area_uniao if area_uniao > 0 else 0.0    area = (x2 - x1 + 1) * (y2 - y1 + 1)

        indices = np.argsort(y2)

    return iou    

    # Continuar iterando enquanto ainda houver índices na lista

    while len(indices) > 0:

def suprimir_nao_maximos(caixas, confiancas, iou_threshold=0.3):        # Pegar o último índice da lista e adicionar à lista de escolhidos

    """        ultimo = len(indices) - 1

    Aplica Non-Maximum Suppression em um conjunto de detecções.        i = indices[ultimo]

            escolhidos.append(i)

    Args:        

        caixas (numpy.ndarray): Array de bounding boxes (N, 4) com formato (x, y, w, h)        # Encontrar as coordenadas (x, y) maiores para o início

        confiancas (numpy.ndarray): Array de scores de confiança (N,)        # e as coordenadas (x, y) menores para o fim da caixa delimitadora

        iou_threshold (float): Limiar de IoU para supressão        xx1 = np.maximum(x1[i], x1[indices[:ultimo]])

                yy1 = np.maximum(y1[i], y1[indices[:ultimo]])

    Returns:        xx2 = np.minimum(x2[i], x2[indices[:ultimo]])

        numpy.ndarray: Índices das caixas mantidas após NMS        yy2 = np.minimum(y2[i], y2[indices[:ultimo]])

    """        

    if len(caixas) == 0:        # Calcular largura e altura da caixa delimitadora

        return np.array([], dtype=int)        w = np.maximum(0, xx2 - xx1 + 1)

            h = np.maximum(0, yy2 - yy1 + 1)

    # Ordenar por confiança (decrescente)        

    indices_ordenados = np.argsort(confiancas)[::-1]        # Calcular razão de sobreposição

            sobreposicao = (w * h) / area[indices[:ultimo]]

    indices_mantidos = []        

            # Deletar todos os índices que têm sobreposição maior que o limiar

    while len(indices_ordenados) > 0:        indices = np.delete(

        # Pegar a caixa com maior confiança            indices,

        idx_atual = indices_ordenados[0]            np.concatenate(([ultimo], np.where(sobreposicao > limiar_sobreposicao)[0]))

        indices_mantidos.append(idx_atual)        )

            

        if len(indices_ordenados) == 1:    # Retornar apenas as caixas delimitadoras escolhidas

            break    return caixas[escolhidos].astype("int")

        

        # Calcular IoU com as demais caixas

        caixa_atual = caixas[idx_atual]def aplicar_nms_em_deteccoes(deteccoes, limiar_sobreposicao=0.3):

        caixas_restantes = caixas[indices_ordenados[1:]]    """

            Aplica NMS em uma lista de detecções e retorna caixas filtradas.

        ious = np.array([calcular_iou(caixa_atual, caixa) for caixa in caixas_restantes])    

            Args:

        # Manter apenas caixas com IoU abaixo do limiar        deteccoes: Lista de dicionários com 'box' (x, y, w, h)

        indices_baixo_iou = np.where(ious < iou_threshold)[0]        limiar_sobreposicao: Limiar de sobreposição IoU

        indices_ordenados = indices_ordenados[1:][indices_baixo_iou]        

        Returns:

    return np.array(indices_mantidos)        Array numpy de caixas filtradas

    """

    if not deteccoes:

def aplicar_nms_em_deteccoes(deteccoes, iou_threshold=0.3):        return np.array([])

    """    

    Aplica NMS em uma lista de detecções.    # Extrair caixas das detecções

        caixas = np.array([d['box'] for d in deteccoes])

    Args:    

        deteccoes (list): Lista de detecções, cada uma com 'bbox' e 'confianca'    # Aplicar NMS

        iou_threshold (float): Limiar de IoU para supressão    caixas_filtradas = suprimir_nao_maximos(caixas, limiar_sobreposicao)

            

    Returns:    return caixas_filtradas

        list: Lista de detecções após NMS
    """
    if not deteccoes:
        return []
    
    # Extrair caixas e confianças
    caixas = np.array([d['bbox'] for d in deteccoes])
    confiancas = np.array([d['confianca'] for d in deteccoes])
    
    # Aplicar NMS
    indices_mantidos = suprimir_nao_maximos(caixas, confiancas, iou_threshold)
    
    # Filtrar detecções
    deteccoes_filtradas = [deteccoes[i] for i in indices_mantidos]
    
    return deteccoes_filtradas
