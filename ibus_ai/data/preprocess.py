""""""

Pré-processamento de ImagensMódulo de Pré-processamento de Imagens

Funções para carregar e pré-processar imagens para detecção de pessoas

Funções para carregar e pré-processar imagens para o pipeline de detecção."""

"""

import cv2

import numpy as npimport numpy as np

from PIL import Imagefrom PIL import Image

import osimport os





def carregar_e_preprocessar_imagem(caminho_imagem, tamanho_alvo=(800, 600)):def carregar_e_preprocessar_imagem(caminho_imagem, tamanho_alvo=(256, 256)):

    """    """

    Carrega e pré-processa uma imagem.    Carrega uma imagem e aplica pré-processamento padrão.

        

    Args:    Etapas de pré-processamento:

        caminho_imagem (str): Caminho para o arquivo de imagem    1. Carrega a imagem do disco

        tamanho_alvo (tuple): Tamanho desejado (largura, altura)    2. Redimensiona para dimensões consistentes

            3. Converte para escala de cinza

    Returns:    4. Normaliza valores dos pixels (0-1)

        numpy.ndarray: Imagem pré-processada como array NumPy (RGB)    

            Args:

    Raises:        caminho_imagem: Caminho para o arquivo de imagem

        FileNotFoundError: Se a imagem não for encontrada        tamanho_alvo: Tupla (largura, altura) para redimensionamento

        ValueError: Se a imagem não puder ser carregada        

    """    Returns:

    if not os.path.exists(caminho_imagem):        Array numpy da imagem pré-processada (normalizada, escala de cinza)

        raise FileNotFoundError(f"Imagem não encontrada: {caminho_imagem}")        ou None se o arquivo não existir

        """

    try:    if not os.path.exists(caminho_imagem):

        # Carregar imagem        print(f"Erro: Arquivo de imagem não encontrado em {caminho_imagem}")

        img = Image.open(caminho_imagem)        return None

            

        # Converter para RGB (caso seja RGBA ou escala de cinza)    # Carregar imagem

        if img.mode != 'RGB':    imagem = Image.open(caminho_imagem)

            img = img.convert('RGB')    

            # Redimensionar imagem

        # Redimensionar se necessário    imagem_redimensionada = imagem.resize(tamanho_alvo)

        if tamanho_alvo is not None:    

            img = img.resize(tamanho_alvo, Image.Resampling.LANCZOS)    # Converter para escala de cinza

            imagem_cinza = imagem_redimensionada.convert('L')  # 'L' para escala de cinza

        # Converter para array NumPy    

        img_array = np.array(img)    # Converter para array numpy e normalizar valores dos pixels

            imagem_array = np.array(imagem_cinza, dtype=np.float32) / 255.0

        return img_array    

            return imagem_array

    except Exception as e:

        raise ValueError(f"Erro ao carregar imagem {caminho_imagem}: {str(e)}")

def criar_imagem_dummy(caminho_saida="imagem_dummy.png", tamanho=(50, 50)):

    """

def criar_imagem_dummy(largura=800, altura=600, cor=(128, 128, 128)):    Cria uma imagem dummy para fins de demonstração.

    """    

    Cria uma imagem dummy para testes.    Args:

            caminho_saida: Caminho onde salvar a imagem dummy

    Args:        tamanho: Tupla (altura, largura) da imagem

        largura (int): Largura da imagem        

        altura (int): Altura da imagem    Returns:

        cor (tuple): Cor RGB da imagem        Caminho da imagem criada

            """

    Returns:    # Criar imagem RGB simples de 3 canais

        numpy.ndarray: Imagem dummy como array NumPy    dados_imagem_dummy = np.random.randint(0, 256, (*tamanho, 3), dtype=np.uint8)

    """    imagem_dummy = Image.fromarray(dados_imagem_dummy)

    img = np.ones((altura, largura, 3), dtype=np.uint8)    imagem_dummy.save(caminho_saida)

    img[:, :] = cor    

    return img    print(f"Imagem dummy salva em: {caminho_saida}")

    return caminho_saida



def carregar_multiplas_imagens(caminhos_imagens, tamanho_alvo=(800, 600), verbose=True):

    """def carregar_multiplas_imagens(caminhos_imagens, tamanho_alvo=(256, 256)):

    Carrega múltiplas imagens de uma lista de caminhos.    """

        Carrega e pré-processa múltiplas imagens.

    Args:    

        caminhos_imagens (list): Lista de caminhos para as imagens    Args:

        tamanho_alvo (tuple): Tamanho desejado (largura, altura)        caminhos_imagens: Lista de caminhos para arquivos de imagem

        verbose (bool): Se True, exibe progresso        tamanho_alvo: Tupla (largura, altura) para redimensionamento

                

    Returns:    Returns:

        list: Lista de imagens como arrays NumPy        Lista de arrays numpy de imagens pré-processadas

            """

    Raises:    imagens_preprocessadas = []

        ValueError: Se nenhuma imagem for carregada com sucesso    

    """    for caminho in caminhos_imagens:

    imagens = []        imagem = carregar_e_preprocessar_imagem(caminho, tamanho_alvo)

    erros = []        if imagem is not None:

                imagens_preprocessadas.append(imagem)

    for i, caminho in enumerate(caminhos_imagens):    

        try:    print(f"Carregadas e pré-processadas {len(imagens_preprocessadas)} imagem(ns).")

            img = carregar_e_preprocessar_imagem(caminho, tamanho_alvo)    return imagens_preprocessadas

            imagens.append(img)
            if verbose:
                print(f"✓ Carregada {i+1}/{len(caminhos_imagens)}: {os.path.basename(caminho)}")
        except Exception as e:
            erros.append((caminho, str(e)))
            if verbose:
                print(f"✗ Erro ao carregar {caminho}: {str(e)}")
    
    if not imagens:
        raise ValueError(f"Nenhuma imagem foi carregada com sucesso. Erros: {erros}")
    
    if verbose and erros:
        print(f"\n⚠ {len(erros)} imagem(ns) não pôde(ram) ser carregada(s)")
    
    return imagens
