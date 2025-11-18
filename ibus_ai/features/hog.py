""""""

Extração de Características HOG (Histogram of Oriented Gradients)Módulo de Extração de Características HOG

Funções para extrair características HOG (Histogram of Oriented Gradients)

HOG é um descritor de características amplamente usado para detecção de objetos."""

"""

from skimage.feature import hog

import numpy as npimport numpy as np

from skimage.feature import hog

from skimage import color

# Parâmetros padrão para HOG

ORIENTACOES_PADRAO = 9

def extrair_hog(imagem, orientacoes=9, pixels_por_celula=(8, 8), celulas_por_bloco=(2, 2),PIXELS_POR_CELULA_PADRAO = (8, 8)

                visualizar=False, transformar_sqrt=True):CELULAS_POR_BLOCO_PADRAO = (2, 2)

    """

    Extrai características HOG de uma imagem.

    def extrair_hog(imagem, orientacoes=ORIENTACOES_PADRAO, 

    Args:                pixels_por_celula=PIXELS_POR_CELULA_PADRAO,

        imagem (numpy.ndarray): Imagem de entrada (RGB ou escala de cinza)                celulas_por_bloco=CELULAS_POR_BLOCO_PADRAO,

        orientacoes (int): Número de bins de orientação                visualizar=False):

        pixels_por_celula (tuple): Tamanho de cada célula em pixels    """

        celulas_por_bloco (tuple): Número de células em cada bloco    Extrai características HOG de uma imagem ou patch.

        visualizar (bool): Se True, retorna também a imagem de visualização do HOG    

        transformar_sqrt (bool): Aplicar normalização por raiz quadrada    HOG (Histogram of Oriented Gradients) descreve a aparência e forma de objetos

            contando ocorrências de gradientes de orientação de borda em porções localizadas.

    Returns:    

        numpy.ndarray: Vetor de características HOG    Args:

        numpy.ndarray (opcional): Imagem de visualização do HOG (se visualizar=True)        imagem: Array numpy da imagem (escala de cinza, normalizada 0-1)

    """        orientacoes: Número de bins de orientação

    # Converter para escala de cinza se necessário        pixels_por_celula: Tamanho da célula (tupla)

    if len(imagem.shape) == 3:        celulas_por_bloco: Número de células por bloco (tupla)

        imagem_gray = color.rgb2gray(imagem)        visualizar: Se True, retorna também a imagem HOG visualizada

    else:        

        imagem_gray = imagem    Returns:

            Vetor de características HOG (array 1D)

    # Extrair HOG        Se visualizar=True, retorna (características, imagem_hog)

    if visualizar:    """

        features, hog_image = hog(    caracteristicas = hog(

            imagem_gray,        imagem,

            orientations=orientacoes,        orientations=orientacoes,

            pixels_per_cell=pixels_por_celula,        pixels_per_cell=pixels_por_celula,

            cells_per_block=celulas_por_bloco,        cells_per_block=celulas_por_bloco,

            transform_sqrt=transformar_sqrt,        visualize=visualizar

            visualize=True,    )

            feature_vector=True    

        )    return caracteristicas

        return features, hog_image

    else:

        features = hog(def extrair_hog_de_rois(imagem, rois, orientacoes=ORIENTACOES_PADRAO,

            imagem_gray,                        pixels_por_celula=PIXELS_POR_CELULA_PADRAO,

            orientations=orientacoes,                        celulas_por_bloco=CELULAS_POR_BLOCO_PADRAO):

            pixels_per_cell=pixels_por_celula,    """

            cells_per_block=celulas_por_bloco,    Extrai características HOG de múltiplas Regiões de Interesse (ROIs).

            transform_sqrt=transformar_sqrt,    

            visualize=False,    Args:

            feature_vector=True        imagem: Imagem pré-processada normalizada (0-1)

        )        rois: Lista de dicionários com 'box' (x, y, w, h) e 'label'

        return features        orientacoes: Número de bins de orientação

        pixels_por_celula: Tamanho da célula

        celulas_por_bloco: Número de células por bloco

def extrair_hog_de_rois(rois, orientacoes=9, pixels_por_celula=(8, 8),         

                        celulas_por_bloco=(2, 2), verbose=True):    Returns:

    """        Tupla (lista_caracteristicas, lista_rotulos)

    Extrai características HOG de múltiplas ROIs.    """

        lista_caracteristicas = []

    Args:    lista_rotulos = []

        rois (list): Lista de regiões (arrays NumPy)    

        orientacoes (int): Número de bins de orientação    for roi in rois:

        pixels_por_celula (tuple): Tamanho de cada célula em pixels        x, y, w, h = roi['box']

        celulas_por_bloco (tuple): Número de células em cada bloco        label = roi['label']

        verbose (bool): Se True, exibe progresso        

                # Extrair o patch da imagem pré-processada

    Returns:        # Fatiamento: [y_inicial:y_final, x_inicial:x_final]

        numpy.ndarray: Matriz de características (n_rois, n_features)        patch = imagem[y : y + h, x : x + w]

    """        

    caracteristicas = []        # Garantir que o patch não está vazio

            if patch.shape[0] > 0 and patch.shape[1] > 0:

    for i, roi in enumerate(rois):            # Extrair características HOG do patch

        try:            caracteristicas = extrair_hog(

            features = extrair_hog(                patch,

                roi,                orientacoes=orientacoes,

                orientacoes=orientacoes,                pixels_por_celula=pixels_por_celula,

                pixels_por_celula=pixels_por_celula,                celulas_por_bloco=celulas_por_bloco,

                celulas_por_bloco=celulas_por_bloco,                visualizar=False

                visualizar=False            )

            )            

            caracteristicas.append(features)            lista_caracteristicas.append(caracteristicas)

                        lista_rotulos.append(label)

            if verbose and (i + 1) % 100 == 0:    

                print(f"Processadas {i+1}/{len(rois)} ROIs")    # Exibir contagem de características extraídas

                    contagem_pessoa = lista_rotulos.count('person')

        except Exception as e:    contagem_nao_pessoa = lista_rotulos.count('non-person')

            if verbose:    

                print(f"⚠ Erro ao processar ROI {i}: {str(e)}")    print(f"Características HOG extraídas para classe 'person': {contagem_pessoa}")

            continue    print(f"Características HOG extraídas para classe 'non-person': {contagem_nao_pessoa}")

        print(f"Total de características HOG extraídas: {len(lista_caracteristicas)}")

    if not caracteristicas:    

        raise ValueError("Nenhuma característica foi extraída com sucesso")    return lista_caracteristicas, lista_rotulos

    

    return np.array(caracteristicas)

def padronizar_caracteristicas(lista_caracteristicas):

    """

def padronizar_caracteristicas(X_train, X_test=None):    Padroniza características para que todas tenham o mesmo comprimento.

    """    Adiciona padding com zeros nas características mais curtas.

    Padroniza características para média 0 e desvio padrão 1.    

        Args:

    Args:        lista_caracteristicas: Lista de arrays de características HOG

        X_train (numpy.ndarray): Características de treino        

        X_test (numpy.ndarray, opcional): Características de teste    Returns:

                Tupla (array 2D numpy padronizado, comprimento máximo usado)

    Returns:    """

        numpy.ndarray: X_train padronizado    # Encontrar o comprimento máximo dos vetores de características

        numpy.ndarray (opcional): X_test padronizado (se fornecido)    comprimento_maximo = max(len(f) for f in lista_caracteristicas)

        tuple: (média, desvio padrão) para usar em novos dados    

    """    # Adicionar padding às características mais curtas

    # Calcular média e desvio padrão do conjunto de treino    caracteristicas_padronizadas = []

    media = np.mean(X_train, axis=0)    for caracteristicas in lista_caracteristicas:

    desvio = np.std(X_train, axis=0)        if len(caracteristicas) < comprimento_maximo:

                # Adicionar zeros ao final

    # Evitar divisão por zero            caracteristicas_pad = np.pad(

    desvio[desvio == 0] = 1.0                caracteristicas,

                    (0, comprimento_maximo - len(caracteristicas)),

    # Padronizar treino                'constant'

    X_train_norm = (X_train - media) / desvio            )

                caracteristicas_padronizadas.append(caracteristicas_pad)

    if X_test is not None:        else:

        # Padronizar teste usando estatísticas do treino            caracteristicas_padronizadas.append(caracteristicas)

        X_test_norm = (X_test - media) / desvio    

        return X_train_norm, X_test_norm, (media, desvio)    # Converter para array numpy 2D

    else:    X = np.array(caracteristicas_padronizadas)

        return X_train_norm, (media, desvio)    

    return X, comprimento_maximo


def aplicar_padronizacao(X, media, desvio):
    """
    Aplica padronização usando média e desvio pré-calculados.
    
    Args:
        X (numpy.ndarray): Características a padronizar
        media (numpy.ndarray): Média calculada do treino
        desvio (numpy.ndarray): Desvio padrão calculado do treino
        
    Returns:
        numpy.ndarray: Características padronizadas
    """
    return (X - media) / desvio
