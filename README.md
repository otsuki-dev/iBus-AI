# iBus-AI: Detecção de Pessoas em Ônibus

Sistema de detecção e contagem de pessoas em interiores de ônibus usando técnicas de visão computacional sem modelos pré-treinados.

## 📋 Visão Geral

Este projeto implementa uma abordagem "do zero" para detectar e contar pessoas em imagens de interiores de ônibus, usando:
- Características HOG (Histogram of Oriented Gradients)
- Classificador SVM (Support Vector Machine)
- Sliding Window para detecção multi-escala
- NMS (Non-Maximum Suppression) para refinar detecções

## 🏗️ Estrutura do Projeto

```
ibus_ai/
├── data/
│   ├── preprocess.py      # Pré-processamento de imagens
│   ├── rois.py            # Gerenciamento de ROIs
│   └── visualizacao.py    # Visualização de resultados
├── features/
│   ├── basicas.py         # Características básicas (bordas, cantos)
│   └── hog.py             # Extração de características HOG
├── models/
│   └── svm.py             # Classificador SVM
├── infer/
│   └── detect.py          # Detecção com sliding window
└── utils/
    └── nms.py             # Supressão não-máxima
```

## 🚀 Como Usar

### 1. Pré-processar uma Imagem

```python
from ibus_ai.data.preprocess import carregar_e_preprocessar_imagem

# Carregar e pré-processar
imagem = carregar_e_preprocessar_imagem('camera-onibus.webp')
```

### 2. Extrair Características

```python
from ibus_ai.features.basicas import extrair_todas_caracteristicas
from ibus_ai.features.hog import extrair_hog_de_rois

# Características básicas
caracteristicas = extrair_todas_caracteristicas(imagem)

# Características HOG de ROIs
from ibus_ai.data.rois import definir_rois_exemplo
rois = definir_rois_exemplo()
lista_hog, rotulos = extrair_hog_de_rois(imagem, rois)
```

### 3. Treinar Classificador

```python
from ibus_ai.models.svm import treinar_classificador_do_zero

classificador, comprimento_max = treinar_classificador_do_zero(lista_hog, rotulos)
```

### 4. Detectar Pessoas

```python
from ibus_ai.infer.detect import sliding_window_deteccao
from ibus_ai.utils.nms import aplicar_nms_em_deteccoes

# Detectar
deteccoes = sliding_window_deteccao(imagem, classificador, comprimento_max)

# Aplicar NMS
caixas_filtradas = aplicar_nms_em_deteccoes(deteccoes, limiar_sobreposicao=0.3)
```

### 5. Visualizar Resultados

```python
from ibus_ai.data.visualizacao import exibir_deteccoes

exibir_deteccoes(imagem, caixas_filtradas, titulo="Pessoas Detectadas")
```

## 📚 Conceitos Implementados

### Características HOG
Descritor que captura gradientes de orientação em células locais, eficaz para detectar formas humanas.

### Classificador SVM
Algoritmo de aprendizado supervisionado que encontra hiperplano ótimo para separar classes.

### Sliding Window
Técnica que desliza uma janela pela imagem em múltiplas escalas para detectar objetos de diferentes tamanhos.

### NMS (Supressão Não-Máxima)
Remove detecções redundantes e sobrepostas, mantendo apenas as mais confiáveis.

## Limitações

Este é um sistema educacional "do zero" com limitações importantes:

- **Dataset Pequeno**: Treinado com poucos exemplos manuais
- **Sensibilidade a Ruído**: Características de baixo nível são sensíveis a variações
- **Oclusão**: Dificuldade com pessoas parcialmente visíveis
- **Iluminação**: Desempenho afetado por mudanças de luz

Para produção, considere usar modelos de deep learning pré-treinados (YOLO, Faster R-CNN).

## 🎓 Propósito Educacional

Este projeto é destinado ao **aprendizado de conceitos fundamentais** de visão computacional:

1. ✅ Pré-processamento de imagens
2. ✅ Extração de características (bordas, cantos, HOG)
3. ✅ Treinamento de classificadores
4. ✅ Detecção multi-escala
5. ✅ Pós-processamento (NMS)

## 📦 Dependências

```bash
pip install -r requirements.txt
```

Principais bibliotecas:
- OpenCV (cv2)
- NumPy
- Pillow (PIL)
- scikit-image
- scikit-learn
- matplotlib

## 🔧 Exemplos

Veja a pasta `examples/` para scripts completos de uso:
- `run_example.py` - Pipeline completo de detecção
- `rois_example.json` - Exemplo de ROIs em JSON

## 📝 Notas de Estudo

Todos os comentários e documentação estão em **português** para facilitar o aprendizado. Cada função possui docstrings explicativas sobre:
- O que a função faz
- Argumentos esperados
- Retornos
- Conceitos teóricos relacionados

## 🤝 Contribuindo

Projeto educacional aberto para melhorias e sugestões!

## 📄 Licença

MIT License - Livre para uso educacional e comercial.
