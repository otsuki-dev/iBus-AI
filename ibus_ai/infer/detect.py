""""""

Detecção com Sliding WindowMódulo de Detecção com Sliding Window

Implementação da abordagem de janela deslizante para detectar pessoas

Implementação de detecção multi-escala usando janela deslizante."""

"""

import numpy as np

import numpy as npfrom skimage.transform import rescale

from skimage.transform import rescalefrom ..features.hog import extrair_hog





def sliding_window_deteccao(imagem, classificador, extrator_features, def sliding_window_deteccao(imagem, classificador, comprimento_caracteristicas,

                            tamanho_janela=(64, 128), passo=16, escala_min=0.5,                             largura_janela=36, altura_janela=50, 

                            escala_max=2.0, num_escalas=5, limiar_confianca=0.0,                            tamanho_passo=8, escalas=[1.0, 0.8, 0.6],

                            verbose=True):                            parametros_hog=None):

    """    """

    Detecta pessoas em uma imagem usando sliding window multi-escala.    Implementa detecção de pessoas usando abordagem de janela deslizante.

        

    Args:    A janela desliza sistematicamente pela imagem em múltiplas escalas,

        imagem (numpy.ndarray): Imagem onde detectar pessoas    extraindo características HOG e classificando cada região.

        classificador: Classificador treinado com método predizer_proba()    

        extrator_features: Função para extrair features de uma região    Args:

        tamanho_janela (tuple): Tamanho (largura, altura) da janela de detecção        imagem: Imagem pré-processada normalizada (0-1)

        passo (int): Tamanho do passo da janela deslizante (em pixels)        classificador: Classificador treinado

        escala_min (float): Escala mínima para detecção        comprimento_caracteristicas: Comprimento esperado do vetor de características

        escala_max (float): Escala máxima para detecção        largura_janela: Largura da janela deslizante

        num_escalas (int): Número de escalas a testar        altura_janela: Altura da janela deslizante

        limiar_confianca (float): Limiar de confiança para detecções        tamanho_passo: Pixels para mover a janela em cada iteração

        verbose (bool): Se True, exibe progresso        escalas: Lista de fatores de escala para detecção multi-escala

                parametros_hog: Dicionário com parâmetros HOG (orientacoes, pixels_por_celula, etc.)

    Returns:        

        list: Lista de detecções, cada uma como dict com:    Returns:

            - 'bbox': (x, y, w, h) na imagem original        Lista de dicionários com detecções {'box': (x, y, w, h), 'scale': escala}

            - 'confianca': score de confiança    """

            - 'escala': escala em que foi detectado    if parametros_hog is None:

    """        from ..features.hog import (ORIENTACOES_PADRAO, PIXELS_POR_CELULA_PADRAO,

    altura_img, largura_img = imagem.shape[:2]                                     CELULAS_POR_BLOCO_PADRAO)

    largura_janela, altura_janela = tamanho_janela        parametros_hog = {

                'orientacoes': ORIENTACOES_PADRAO,

    # Gerar escalas            'pixels_por_celula': PIXELS_POR_CELULA_PADRAO,

    escalas = np.linspace(escala_min, escala_max, num_escalas)            'celulas_por_bloco': CELULAS_POR_BLOCO_PADRAO

            }

    deteccoes = []    

        deteccoes = []

    for i, escala in enumerate(escalas):    

        if verbose:    print("Iniciando detecção com janela deslizante...")

            print(f"🔍 Processando escala {i+1}/{num_escalas}: {escala:.2f}x")    

            # Iterar sobre cada fator de escala

        # Redimensionar imagem    for escala in escalas:

        if escala != 1.0:        # Redimensionar a imagem pelo fator de escala atual

            img_redim = rescale(imagem, escala, anti_aliasing=True,         imagem_escalada = rescale(imagem, escala, anti_aliasing=False, channel_axis=None)

                              channel_axis=2 if len(imagem.shape) == 3 else None)        

            # Converter de volta para uint8        # Garantir que a imagem escalada seja grande o suficiente para a janela

            if img_redim.max() <= 1.0:        if imagem_escalada.shape[0] < altura_janela or imagem_escalada.shape[1] < largura_janela:

                img_redim = (img_redim * 255).astype(np.uint8)            continue

        else:        

            img_redim = imagem        # Iterar sobre a imagem redimensionada usando janela deslizante

                for y in range(0, imagem_escalada.shape[0] - altura_janela + 1, tamanho_passo):

        altura_redim, largura_redim = img_redim.shape[:2]            for x in range(0, imagem_escalada.shape[1] - largura_janela + 1, tamanho_passo):

                        # Extrair o patch da janela

        # Sliding window                patch = imagem_escalada[y : y + altura_janela, x : x + largura_janela]

        num_deteccoes_escala = 0                

        for y in range(0, altura_redim - altura_janela, passo):                # Calcular características HOG para o patch

            for x in range(0, largura_redim - largura_janela, passo):                caracteristicas_patch = extrair_hog(

                # Extrair janela                    patch,

                janela = img_redim[y:y+altura_janela, x:x+largura_janela]                    orientacoes=parametros_hog['orientacoes'],

                                    pixels_por_celula=parametros_hog['pixels_por_celula'],

                # Verificar tamanho                    celulas_por_bloco=parametros_hog['celulas_por_bloco'],

                if janela.shape[:2] != (altura_janela, largura_janela):                    visualizar=False

                    continue                )

                                

                # Extrair features                # Adicionar padding às características HOG

                try:                caracteristicas_padronizadas = np.pad(

                    features = extrator_features(janela)                    caracteristicas_patch,

                    features = features.reshape(1, -1)                    (0, comprimento_caracteristicas - len(caracteristicas_patch)),

                except Exception as e:                    'constant'

                    continue                )

                                

                # Predizer                # Usar o classificador para prever se o patch contém uma 'pessoa'

                confianca = classificador.predizer_proba(features)[0]                predicao = classificador.prever(caracteristicas_padronizadas.reshape(1, -1))

                                

                # Se acima do limiar, adicionar detecção                # Se a previsão for 'pessoa', calcular coordenadas originais e adicionar às detecções

                if confianca > limiar_confianca:                if predicao[0] == 'person':

                    # Converter coordenadas de volta para escala original                    x_original = int(x / escala)

                    x_orig = int(x / escala)                    y_original = int(y / escala)

                    y_orig = int(y / escala)                    w_original = int(largura_janela / escala)

                    w_orig = int(largura_janela / escala)                    h_original = int(altura_janela / escala)

                    h_orig = int(altura_janela / escala)                    

                                        deteccoes.append({

                    deteccoes.append({                        'box': (x_original, y_original, w_original, h_original),

                        'bbox': (x_orig, y_orig, w_orig, h_orig),                        'scale': escala

                        'confianca': float(confianca),                    })

                        'escala': float(escala)    

                    })    print(f"Detecção com janela deslizante concluída. Encontradas {len(deteccoes)} detecções potenciais.")

                    num_deteccoes_escala += 1    

            return deteccoes

        if verbose:

            print(f"  → {num_deteccoes_escala} detecções nesta escala")

    def extrair_caixas_de_deteccoes(deteccoes):

    if verbose:    """

        print(f"\n✅ Total de {len(deteccoes)} detecções brutas")    Extrai apenas as caixas delimitadoras das detecções.

        

    return deteccoes    Args:

        deteccoes: Lista de dicionários com 'box' e 'scale'

        

def extrair_caixas_de_deteccoes(deteccoes):    Returns:

    """        Array numpy de caixas (N x 4) no formato [x, y, w, h]

    Extrai apenas as bounding boxes das detecções.    """

        if not deteccoes:

    Args:        return np.array([])

        deteccoes (list): Lista de detecções    

            caixas = np.array([d['box'] for d in deteccoes])

    Returns:    return caixas

        numpy.ndarray: Array de bounding boxes (N, 4) com formato (x, y, w, h)
        numpy.ndarray: Array de confianças (N,)
    """
    if not deteccoes:
        return np.array([]), np.array([])
    
    caixas = np.array([d['bbox'] for d in deteccoes])
    confiancas = np.array([d['confianca'] for d in deteccoes])
    
    return caixas, confiancas


def detectar_pessoas_multiescala(imagem, classificador, extrator_features,
                                 aplicar_nms=True, iou_threshold=0.3,
                                 **kwargs):
    """
    Pipeline completo de detecção com NMS opcional.
    
    Args:
        imagem (numpy.ndarray): Imagem onde detectar pessoas
        classificador: Classificador treinado
        extrator_features: Função para extrair features
        aplicar_nms (bool): Se True, aplica Non-Maximum Suppression
        iou_threshold (float): Limiar de IoU para NMS
        **kwargs: Argumentos adicionais para sliding_window_deteccao
        
    Returns:
        list: Lista de detecções finais (após NMS se aplicável)
    """
    # Detecção multi-escala
    deteccoes = sliding_window_deteccao(
        imagem, classificador, extrator_features, **kwargs
    )
    
    if not deteccoes:
        return []
    
    # Aplicar NMS se solicitado
    if aplicar_nms:
        from ..utils.nms import aplicar_nms_em_deteccoes
        deteccoes = aplicar_nms_em_deteccoes(deteccoes, iou_threshold)
    
    return deteccoes
