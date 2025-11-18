# 🗺️ Mapeamento: Notebook → Módulos

Este documento mostra onde cada parte do notebook original `iBus.ipynb` foi reorganizada nos novos módulos.

---

## 📓 Células do Notebook → Módulos Python

### Seção 1: Pré-processamento de Imagens

| Notebook Original | Novo Módulo | Função |
|-------------------|-------------|---------|
| Células de importação (PIL, numpy, matplotlib) | `ibus_ai/data/preprocess.py` | Imports no topo |
| Criar imagem dummy | `criar_imagem_dummy()` | `ibus_ai/data/preprocess.py` |
| Carregar imagens | `carregar_e_preprocessar_imagem()` | `ibus_ai/data/preprocess.py` |
| Redimensionar para 256x256 | Dentro de `carregar_e_preprocessar_imagem()` | `ibus_ai/data/preprocess.py` |
| Converter para escala de cinza | Dentro de `carregar_e_preprocessar_imagem()` | `ibus_ai/data/preprocess.py` |
| Normalizar pixels (0-1) | Dentro de `carregar_e_preprocessar_imagem()` | `ibus_ai/data/preprocess.py` |
| Exibir imagem pré-processada | `exibir_imagem_preprocessada()` | `ibus_ai/data/visualizacao.py` |

---

### Seção 2: Extração de Características Básicas

| Notebook Original | Novo Módulo | Função |
|-------------------|-------------|---------|
| Import cv2 | `ibus_ai/features/basicas.py` | Import no topo |
| Aplicar Canny edge detector | `detectar_bordas_canny()` | `ibus_ai/features/basicas.py` |
| Aplicar Harris corner detector | `detectar_cantos_harris()` | `ibus_ai/features/basicas.py` |
| Calcular histograma de intensidade | `calcular_histograma_intensidade()` | `ibus_ai/features/basicas.py` |
| Exibir características em subplots | `exibir_caracteristicas()` | `ibus_ai/data/visualizacao.py` |
| Extrair todas de uma vez | `extrair_todas_caracteristicas()` | `ibus_ai/features/basicas.py` |

---

### Seção 3: Definição de ROIs

| Notebook Original | Novo Módulo | Função |
|-------------------|-------------|---------|
| Lista de ROIs manualmente definidas | `definir_rois_exemplo()` | `ibus_ai/data/rois.py` |
| Desenhar retângulos nas ROIs | `exibir_rois()` | `ibus_ai/data/visualizacao.py` |
| Adicionar labels nas ROIs | Dentro de `exibir_rois()` | `ibus_ai/data/visualizacao.py` |
| Salvar ROIs (não estava no notebook) | `salvar_rois_json()` | `ibus_ai/data/rois.py` |
| Carregar ROIs (não estava no notebook) | `carregar_rois_json()` | `ibus_ai/data/rois.py` |
| Validar ROIs (não estava no notebook) | `validar_rois()` | `ibus_ai/data/rois.py` |

---

### Seção 4: Extração de Características HOG

| Notebook Original | Novo Módulo | Função |
|-------------------|-------------|---------|
| Import skimage.feature.hog | `ibus_ai/features/hog.py` | Import no topo |
| Definir parâmetros HOG (orientations, etc.) | Constantes globais | `ibus_ai/features/hog.py` |
| Iterar sobre ROIs | `extrair_hog_de_rois()` | `ibus_ai/features/hog.py` |
| Extrair patch de cada ROI | Dentro de `extrair_hog_de_rois()` | `ibus_ai/features/hog.py` |
| Calcular HOG do patch | `extrair_hog()` | `ibus_ai/features/hog.py` |
| Armazenar features e labels | Retorno de `extrair_hog_de_rois()` | `ibus_ai/features/hog.py` |
| Padding de features | `padronizar_caracteristicas()` | `ibus_ai/features/hog.py` |

---

### Seção 5: Treinamento do Classificador SVM

| Notebook Original | Novo Módulo | Função |
|-------------------|-------------|---------|
| Import sklearn.svm.LinearSVC | `ibus_ai/models/svm.py` | Import no topo |
| Converter listas para numpy arrays | `padronizar_caracteristicas()` | `ibus_ai/features/hog.py` |
| Adicionar padding às features | Dentro de `padronizar_caracteristicas()` | `ibus_ai/features/hog.py` |
| Instanciar LinearSVC | `ClassificadorPessoas.__init__()` | `ibus_ai/models/svm.py` |
| Treinar classificador (.fit) | `ClassificadorPessoas.treinar()` | `ibus_ai/models/svm.py` |
| Pipeline completo de treinamento | `treinar_classificador_do_zero()` | `ibus_ai/models/svm.py` |

---

### Seção 6: Sliding Window Detection

| Notebook Original | Novo Módulo | Função |
|-------------------|-------------|---------|
| Import skimage.transform.rescale | `ibus_ai/infer/detect.py` | Import no topo |
| Definir parâmetros da janela | Argumentos de função | `ibus_ai/infer/detect.py` |
| Definir escalas [1.0, 0.8, 0.6] | Argumentos de função | `ibus_ai/infer/detect.py` |
| Loop sobre escalas | `sliding_window_deteccao()` | `ibus_ai/infer/detect.py` |
| Redimensionar imagem (rescale) | Dentro de `sliding_window_deteccao()` | `ibus_ai/infer/detect.py` |
| Loop de sliding window (y, x) | Dentro de `sliding_window_deteccao()` | `ibus_ai/infer/detect.py` |
| Extrair patch da janela | Dentro de `sliding_window_deteccao()` | `ibus_ai/infer/detect.py` |
| Calcular HOG do patch | Chamada a `extrair_hog()` | `ibus_ai/features/hog.py` |
| Padding de features | Dentro de `sliding_window_deteccao()` | `ibus_ai/infer/detect.py` |
| Classificar patch | Chamada a `classificador.prever()` | `ibus_ai/models/svm.py` |
| Calcular coordenadas originais | Dentro de `sliding_window_deteccao()` | `ibus_ai/infer/detect.py` |
| Armazenar detecções | Retorno de `sliding_window_deteccao()` | `ibus_ai/infer/detect.py` |

---

### Seção 7: Supressão Não-Máxima (NMS)

| Notebook Original | Novo Módulo | Função |
|-------------------|-------------|---------|
| Função non_max_suppression completa | `suprimir_nao_maximos()` | `ibus_ai/utils/nms.py` |
| Converter caixas para float | Dentro de `suprimir_nao_maximos()` | `ibus_ai/utils/nms.py` |
| Calcular área das caixas | Dentro de `suprimir_nao_maximos()` | `ibus_ai/utils/nms.py` |
| Ordenar por coordenada y | Dentro de `suprimir_nao_maximos()` | `ibus_ai/utils/nms.py` |
| Loop de supressão | Dentro de `suprimir_nao_maximos()` | `ibus_ai/utils/nms.py` |
| Calcular sobreposição (IoU) | Dentro de `suprimir_nao_maximos()` | `ibus_ai/utils/nms.py` |
| Deletar índices sobrepostos | Dentro de `suprimir_nao_maximos()` | `ibus_ai/utils/nms.py` |
| Preparar detecções para NMS | `aplicar_nms_em_deteccoes()` | `ibus_ai/utils/nms.py` |
| Extrair caixas das detecções | Dentro de `aplicar_nms_em_deteccoes()` | `ibus_ai/utils/nms.py` |

---

### Seção 8: Visualização de Resultados

| Notebook Original | Novo Módulo | Função |
|-------------------|-------------|---------|
| Desenhar retângulos nas detecções | `exibir_deteccoes()` | `ibus_ai/data/visualizacao.py` |
| Converter imagem para BGR/RGB | Dentro de `exibir_deteccoes()` | `ibus_ai/data/visualizacao.py` |
| Exibir com matplotlib | Dentro de `exibir_deteccoes()` | `ibus_ai/data/visualizacao.py` |
| Adicionar título com contagem | Dentro de `exibir_deteccoes()` | `ibus_ai/data/visualizacao.py` |

---

## 📊 Estatísticas da Reorganização

### Notebook Original:
- **1 arquivo**: iBus.ipynb
- **1084 linhas**: Tudo misturado
- **Células**: ~30 células código + markdown
- **Idioma**: Inglês/Português misturado

### Módulos Novos:
- **8 arquivos Python**: Organizados por funcionalidade
- **~800 linhas de código**: Bem documentado
- **100% em Português**: Comentários, docstrings, nomes
- **3 arquivos de documentação**: README, Guia, Tutorial
- **1 notebook educacional**: Tutorial completo
- **1 script de exemplo**: Pipeline completo

---

## 🔄 Fluxo de Execução: Notebook vs. Módulos

### ❌ Notebook Original (Sequencial):

```
Célula 1: Importar bibliotecas
Célula 2: Criar dummy image
Célula 3: Carregar e pré-processar
Célula 4: Exibir imagem
Célula 5: Importar cv2
Célula 6: Detectar bordas, cantos, histograma
Célula 7: Exibir características
Célula 8: Definir ROIs
Célula 9: Desenhar ROIs
Célula 10: Importar skimage.hog
Célula 11: Extrair HOG de ROIs
Célula 12: Importar sklearn.svm
Célula 13: Padronizar features
Célula 14: Treinar SVM
Célula 15: Importar rescale
Célula 16: Sliding window detection
Célula 17: Definir função NMS
Célula 18: Aplicar NMS
Célula 19: Visualizar resultados
```

### ✅ Módulos Organizados (Modular):

```python
# Pipeline em ~20 linhas!

from ibus_ai.data.preprocess import carregar_e_preprocessar_imagem
from ibus_ai.data.rois import definir_rois_exemplo
from ibus_ai.features.hog import extrair_hog_de_rois
from ibus_ai.models.svm import treinar_classificador_do_zero
from ibus_ai.infer.detect import sliding_window_deteccao
from ibus_ai.utils.nms import aplicar_nms_em_deteccoes
from ibus_ai.data.visualizacao import exibir_deteccoes

# Pipeline
imagem = carregar_e_preprocessar_imagem('cameras-onibus.webp')
rois = definir_rois_exemplo()
lista_hog, rotulos = extrair_hog_de_rois(imagem, rois)
classificador, comp_max = treinar_classificador_do_zero(lista_hog, rotulos)
deteccoes = sliding_window_deteccao(imagem, classificador, comp_max)
caixas = aplicar_nms_em_deteccoes(deteccoes)
exibir_deteccoes(imagem, caixas)
```

**Muito mais limpo e legível! 🎉**

---

## 🎯 Benefícios da Modularização

### 1. Reutilização
**Antes:** Copiar e colar células inteiras
**Depois:** Import simples da função

### 2. Manutenção
**Antes:** Procurar em 1084 linhas qual célula modificar
**Depois:** Ir direto no arquivo/função específica

### 3. Testabilidade
**Antes:** Difícil testar partes isoladas
**Depois:** Cada função pode ser testada independentemente

### 4. Colaboração
**Antes:** Conflitos de merge em notebooks são terríveis
**Depois:** Múltiplas pessoas podem trabalhar em módulos diferentes

### 5. Documentação
**Antes:** Markdown misturado com código
**Depois:** Docstrings + arquivos MD separados

### 6. Aprendizado
**Antes:** Difícil entender o fluxo geral
**Depois:** Estudar um módulo de cada vez, na ordem lógica

---

## 📚 Onde Encontrar Cada Conceito

| Conceito | Onde Está Explicado |
|----------|---------------------|
| Pré-processamento de imagens | `GUIA_DE_ESTUDO.md` → Seção "data/preprocess.py" |
| Detecção de bordas Canny | `GUIA_DE_ESTUDO.md` → Seção "features/basicas.py" |
| Detecção de cantos Harris | `GUIA_DE_ESTUDO.md` → Seção "features/basicas.py" |
| HOG (teoria completa) | `GUIA_DE_ESTUDO.md` → Seção "features/hog.py" |
| SVM (teoria completa) | `GUIA_DE_ESTUDO.md` → Seção "models/svm.py" |
| Sliding Window | `GUIA_DE_ESTUDO.md` → Seção "infer/detect.py" |
| NMS (teoria completa) | `GUIA_DE_ESTUDO.md` → Seção "utils/nms.py" |
| Exemplos práticos | `tutorial_completo.ipynb` |
| Pipeline completo | `examples/run_example.py` |
| Uso geral | `README.md` |

---

## 🚀 Como Começar a Usar

### Opção 1: Script Python
```bash
cd examples
python run_example.py
```

### Opção 2: Notebook Educacional
```bash
jupyter notebook notebooks/tutorial_completo.ipynb
```

### Opção 3: Importar em Seu Código
```python
# Seu próprio script ou notebook
from ibus_ai.data.preprocess import carregar_e_preprocessar_imagem

imagem = carregar_e_preprocessar_imagem('sua_imagem.jpg')
# ... continuar com o pipeline
```

---

## 💡 Dica de Estudo

**Ordem recomendada para estudar os módulos:**

1. 📖 Ler `REORGANIZACAO_RESUMO.md` (este arquivo!)
2. 📖 Ler `README.md` para visão geral
3. 📖 Ler `GUIA_DE_ESTUDO.md` para teoria detalhada
4. 💻 Executar `examples/run_example.py`
5. 📓 Seguir `notebooks/tutorial_completo.ipynb`
6. 🔍 Explorar cada módulo em `ibus_ai/`:
   - Começar por `data/preprocess.py`
   - Depois `features/basicas.py`
   - Depois `features/hog.py`
   - Depois `models/svm.py`
   - Depois `infer/detect.py`
   - Depois `utils/nms.py`
   - Por fim `data/visualizacao.py`
7. 🧪 Experimentar com suas próprias modificações!

---

## ✅ Checklist de Conclusão

Use este checklist para acompanhar seu progresso:

- [ ] Li o `REORGANIZACAO_RESUMO.md`
- [ ] Li o `README.md`
- [ ] Executei `run_example.py` com sucesso
- [ ] Segui o `tutorial_completo.ipynb` completamente
- [ ] Entendi o módulo `data/preprocess.py`
- [ ] Entendi o módulo `features/basicas.py`
- [ ] Entendi o módulo `features/hog.py`
- [ ] Entendi o módulo `models/svm.py`
- [ ] Entendi o módulo `infer/detect.py`
- [ ] Entendi o módulo `utils/nms.py`
- [ ] Entendi o módulo `data/visualizacao.py`
- [ ] Li todo o `GUIA_DE_ESTUDO.md`
- [ ] Experimentei modificar parâmetros
- [ ] Testei com minhas próprias imagens
- [ ] Criei minhas próprias ROIs

---

**Parabéns! Agora você tem um projeto bem organizado e pronto para estudar! 🎉📚**
