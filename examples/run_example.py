""""""

Exemplo de Uso do iBus-AIScript de Exemplo: Pipeline Completo de Detecção de Pessoas

Demonstra o uso de todos os módulos do iBus-AI

Este script demonstra como usar o sistema de detecção de pessoas em ônibus."""

"""

import sys

import numpy as npimport os

from ibus_ai.data.preprocess import criar_imagem_dummy

from ibus_ai.data.rois import gerar_negativos_da_imagem# Adicionar o diretório raiz ao path para imports

from ibus_ai.features.hog import extrair_hog, extrair_hog_de_roissys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ibus_ai.models.svm import treinar_classificador_do_zero, avaliar_classificador

from ibus_ai.infer.detect import detectar_pessoas_multiescalafrom ibus_ai.data.preprocess import carregar_e_preprocessar_imagem

from ibus_ai.data.rois import definir_rois_exemplo, salvar_rois_json

from ibus_ai.data.visualizacao import (exibir_imagem_preprocessada, 

def exemplo_completo():                                        exibir_caracteristicas,

    """                                        exibir_rois,

    Exemplo completo do pipeline de detecção.                                        exibir_deteccoes)

    """from ibus_ai.features.basicas import (detectar_bordas_canny, 

    print("=" * 60)                                       detectar_cantos_harris,

    print("EXEMPLO COMPLETO - SISTEMA DE DETECÇÃO DE PESSOAS")                                       calcular_histograma_intensidade)

    print("=" * 60)from ibus_ai.features.hog import extrair_hog_de_rois

    from ibus_ai.models.svm import treinar_classificador_do_zero

    # ========================================from ibus_ai.infer.detect import sliding_window_deteccao

    # PASSO 1: Criar Dados de Exemplofrom ibus_ai.utils.nms import aplicar_nms_em_deteccoes

    # ========================================

    print("\n📦 PASSO 1: Criando dados de exemplo...")

    def executar_pipeline_completo(caminho_imagem):

    # Criar imagem dummy    """

    imagem_teste = criar_imagem_dummy(800, 600, (150, 150, 150))    Executa o pipeline completo de detecção de pessoas.

    print(f"  ✓ Imagem criada: {imagem_teste.shape}")    

        Args:

    # Simular ROIs positivas (pessoas)        caminho_imagem: Caminho para a imagem de entrada

    rois_positivas_exemplo = [    """

        {'x': 100, 'y': 50, 'w': 64, 'h': 128, 'label': 'pessoa'},    print("=" * 70)

        {'x': 300, 'y': 100, 'w': 64, 'h': 128, 'label': 'pessoa'},    print("PIPELINE COMPLETO DE DETECÇÃO DE PESSOAS - iBus-AI")

        {'x': 500, 'y': 150, 'w': 64, 'h': 128, 'label': 'pessoa'},    print("=" * 70)

    ]    

        # ==================== ETAPA 1: PRÉ-PROCESSAMENTO ====================

    # Gerar ROIs positivas (extrair regiões)    print("\n[ETAPA 1] Pré-processamento da imagem...")

    rois_positivas = []    imagem = carregar_e_preprocessar_imagem(caminho_imagem)

    for roi in rois_positivas_exemplo:    

        x, y, w, h = roi['x'], roi['y'], roi['w'], roi['h']    if imagem is None:

        regiao = imagem_teste[y:y+h, x:x+w]        print(f"Erro: Não foi possível carregar a imagem de {caminho_imagem}")

        # Adicionar variação para simular pessoas reais        return

        ruido = np.random.randint(-20, 20, regiao.shape, dtype=np.int16)    

        regiao = np.clip(regiao.astype(np.int16) + ruido, 0, 255).astype(np.uint8)    print(f"✓ Imagem carregada e pré-processada: {imagem.shape}")

        rois_positivas.append(regiao)    exibir_imagem_preprocessada(imagem, "Imagem Pré-processada")

        

    print(f"  ✓ {len(rois_positivas)} ROIs positivas (pessoas)")    # ==================== ETAPA 2: EXTRAÇÃO DE CARACTERÍSTICAS BÁSICAS ====================

        print("\n[ETAPA 2] Extração de características básicas...")

    # Gerar ROIs negativas (não-pessoas)    

    rois_negativas = gerar_negativos_da_imagem(    # Detectar bordas

        imagem_teste,     bordas = detectar_bordas_canny(imagem)

        rois_positivas_exemplo,    print(f"✓ Bordas Canny detectadas")

        tamanho_janela=(64, 128),    

        num_negativos=10    # Detectar cantos

    )    cantos, _ = detectar_cantos_harris(imagem)

    print(f"  ✓ {len(rois_negativas)} ROIs negativas (não-pessoas)")    print(f"✓ Cantos Harris detectados")

        

    # ========================================    # Calcular histograma

    # PASSO 2: Extrair Características HOG    histograma = calcular_histograma_intensidade(imagem)

    # ========================================    print(f"✓ Histograma de intensidade calculado")

    print("\n🔍 PASSO 2: Extraindo características HOG...")    

        # Exibir todas as características

    # Extrair HOG das ROIs positivas    exibir_caracteristicas(imagem, bordas, cantos, histograma)

    X_positivos = extrair_hog_de_rois(rois_positivas, verbose=False)    

    print(f"  ✓ Features positivas: {X_positivos.shape}")    # ==================== ETAPA 3: DEFINIR ROIs ====================

        print("\n[ETAPA 3] Definindo Regiões de Interesse (ROIs)...")

    # Extrair HOG das ROIs negativas    rois = definir_rois_exemplo()

    X_negativos = extrair_hog_de_rois(rois_negativas, verbose=False)    print(f"✓ {len(rois)} ROIs definidas")

    print(f"  ✓ Features negativas: {X_negativos.shape}")    

        # Salvar ROIs em JSON para referência futura

    # ========================================    caminho_rois = os.path.join('examples', 'rois_example.json')

    # PASSO 3: Treinar Classificador SVM    salvar_rois_json(rois, caminho_rois)

    # ========================================    

    print("\n🤖 PASSO 3: Treinando classificador SVM...")    # Visualizar ROIs

        exibir_rois(imagem, rois)

    classificador = treinar_classificador_do_zero(    

        X_positivos,     # ==================== ETAPA 4: EXTRAÇÃO DE CARACTERÍSTICAS HOG ====================

        X_negativos,    print("\n[ETAPA 4] Extraindo características HOG das ROIs...")

        C=1.0,    lista_caracteristicas, lista_rotulos = extrair_hog_de_rois(imagem, rois)

        verbose=True    print(f"✓ Características HOG extraídas de {len(lista_caracteristicas)} ROIs")

    )    

        # ==================== ETAPA 5: TREINAMENTO DO CLASSIFICADOR ====================

    # ========================================    print("\n[ETAPA 5] Treinando classificador SVM...")

    # PASSO 4: Avaliar Classificador    classificador, comprimento_max = treinar_classificador_do_zero(

    # ========================================        lista_caracteristicas, 

    print("\n📊 PASSO 4: Avaliando classificador...")        lista_rotulos

        )

    # Criar conjunto de teste (usando os mesmos dados para demonstração)    print(f"✓ Classificador treinado (comprimento características: {comprimento_max})")

    X_test = np.vstack([X_positivos[:2], X_negativos[:5]])    

    y_test = np.array([1, 1, 0, 0, 0, 0, 0])    # ==================== ETAPA 6: DETECÇÃO COM SLIDING WINDOW ====================

        print("\n[ETAPA 6] Detectando pessoas com Sliding Window...")

    metricas = avaliar_classificador(classificador, X_test, y_test, verbose=True)    deteccoes = sliding_window_deteccao(

            imagem, 

    # ========================================        classificador, 

    # PASSO 5: Detecção em Nova Imagem        comprimento_max,

    # ========================================        largura_janela=36,

    print("\n🎯 PASSO 5: Detectando pessoas em nova imagem...")        altura_janela=50,

            tamanho_passo=8,

    # Criar nova imagem para detecção        escalas=[1.0, 0.8, 0.6]

    imagem_deteccao = criar_imagem_dummy(640, 480, (130, 140, 150))    )

        print(f"✓ {len(deteccoes)} detecções brutas encontradas")

    # Função wrapper para extrator de features    

    def extrator_hog(img):    # ==================== ETAPA 7: APLICAÇÃO DE NMS ====================

        return extrair_hog(img, visualizar=False)    print("\n[ETAPA 7] Aplicando Supressão Não-Máxima (NMS)...")

        caixas_filtradas = aplicar_nms_em_deteccoes(

    # Detectar pessoas        deteccoes, 

    deteccoes = detectar_pessoas_multiescala(        limiar_sobreposicao=0.3

        imagem_deteccao,    )

        classificador,    print(f"✓ {len(caixas_filtradas)} detecções após NMS")

        extrator_hog,    

        tamanho_janela=(64, 128),    # ==================== ETAPA 8: VISUALIZAÇÃO FINAL ====================

        passo=32,    print("\n[ETAPA 8] Visualizando resultados finais...")

        escala_min=0.8,    exibir_deteccoes(

        escala_max=1.5,        imagem, 

        num_escalas=3,        caixas_filtradas, 

        limiar_confianca=0.5,        titulo="Detecção Final de Pessoas"

        aplicar_nms=True,    )

        iou_threshold=0.3,    

        verbose=True    # ==================== RESUMO ====================

    )    print("\n" + "=" * 70)

        print("RESUMO DOS RESULTADOS")

    print(f"\n✅ {len(deteccoes)} pessoas detectadas!")    print("=" * 70)

        print(f"Imagem processada: {caminho_imagem}")

    if deteccoes:    print(f"Dimensões: {imagem.shape[1]} x {imagem.shape[0]} pixels")

        print("\nDetecções:")    print(f"ROIs de treinamento: {len(rois)} ({lista_rotulos.count('person')} pessoas, {lista_rotulos.count('non-person')} não-pessoas)")

        for i, det in enumerate(deteccoes):    print(f"Detecções brutas: {len(deteccoes)}")

            x, y, w, h = det['bbox']    print(f"Detecções após NMS: {len(caixas_filtradas)}")

            conf = det['confianca']    print(f"Taxa de redução NMS: {((len(deteccoes) - len(caixas_filtradas)) / len(deteccoes) * 100):.1f}%")

            print(f"  {i+1}. Posição: ({x}, {y}), Tamanho: {w}x{h}, Confiança: {conf:.2f}")    print("=" * 70)

        print("\n✓ Pipeline concluído com sucesso!")

    # ========================================

    # PASSO 6: Salvar Modelo (Opcional)

    # ========================================if __name__ == "__main__":

    print("\n💾 PASSO 6: Salvando modelo...")    # Caminho da imagem (ajuste conforme necessário)

        caminho_imagem = "cameras-onibus.webp"

    try:    

        classificador.salvar('modelo_pessoas.pkl')    # Verificar se o arquivo existe

        print("  ✓ Modelo salvo em 'modelo_pessoas.pkl'")    if not os.path.exists(caminho_imagem):

    except Exception as e:        print(f"Atenção: Arquivo '{caminho_imagem}' não encontrado no diretório atual.")

        print(f"  ⚠ Erro ao salvar modelo: {e}")        print("Por favor, ajuste o caminho da imagem no script ou coloque a imagem no diretório correto.")

        else:

    print("\n" + "=" * 60)        # Executar pipeline completo

    print("✅ EXEMPLO CONCLUÍDO COM SUCESSO!")        executar_pipeline_completo(caminho_imagem)

    print("=" * 60)


if __name__ == "__main__":
    exemplo_completo()
