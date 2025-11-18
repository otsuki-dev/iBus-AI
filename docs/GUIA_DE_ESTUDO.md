# 📚 Guia de Estudo: iBus-AI

## Visão Geral do Projeto

O iBus-AI é um projeto educacional que implementa um sistema de detecção de pessoas **do zero**, sem usar modelos pré-treinados. O objetivo é aprender os fundamentos da visão computacional.

---

## 🗂️ Estrutura dos Módulos

### 1. `ibus_ai/data/` - Gerenciamento de Dados

#### `preprocess.py` - Pré-processamento de Imagens
**Conceitos aprendidos:**
- Redimensionamento de imagens
- Conversão para escala de cinza
- Normalização de pixels (0-1)

**Funções principais:**
- `carregar_e_preprocessar_imagem()` - Pipeline completo
- `criar_imagem_dummy()` - Para testes
- `carregar_multiplas_imagens()` - Processamento em lote

**Por que é importante?**
Padronizar imagens garante que o modelo receba entrada consistente, independente da fonte original.

---

#### `rois.py` - Regiões de Interesse
**Conceitos aprendidos:**
- Anotação manual de dados
- Formato de caixas delimitadoras (bounding boxes)
- Validação de dados

**Funções principais:**
- `definir_rois_exemplo()` - ROIs pré-definidas
- `salvar_rois_json()` / `carregar_rois_json()` - Persistência
- `validar_rois()` - Verificação de integridade

**Por que é importante?**
ROIs são a "verdade fundamental" (ground truth) que o modelo usa para aprender o que é uma pessoa.

---

#### `visualizacao.py` - Visualização de Resultados
**Conceitos aprendidos:**
- Matplotlib para plotagem
- OpenCV para desenho em imagens
- Conversão de espaços de cor (BGR/RGB)

**Funções principais:**
- `exibir_imagem_preprocessada()` - Mostrar imagem processada
- `exibir_caracteristicas()` - Visualizar bordas/cantos/histograma
- `exibir_rois()` - Mostrar anotações
- `exibir_deteccoes()` - Resultado final

**Por que é importante?**
Visualização ajuda a entender o que cada etapa do pipeline está fazendo.

---

### 2. `ibus_ai/features/` - Extração de Características

#### `basicas.py` - Características de Baixo Nível
**Conceitos aprendidos:**
- Detecção de bordas Canny
- Detecção de cantos Harris
- Histogramas de intensidade

**Funções principais:**
- `detectar_bordas_canny()` - Contornos de objetos
- `detectar_cantos_harris()` - Pontos de interesse
- `calcular_histograma_intensidade()` - Distribuição de pixels

**Por que é importante?**
Essas características são os "blocos de construção" básicos da visão computacional.

**Teoria:**
- **Bordas**: Mudanças abruptas de intensidade indicam limites de objetos
- **Cantos**: Pontos onde bordas mudam de direção (articulações, olhos, etc.)
- **Histograma**: Descreve a distribuição geral de brilho na imagem

---

#### `hog.py` - Características HOG
**Conceitos aprendidos:**
- HOG (Histogram of Oriented Gradients)
- Gradientes de orientação
- Normalização de blocos

**Funções principais:**
- `extrair_hog()` - Extração básica
- `extrair_hog_de_rois()` - Extração de múltiplas regiões
- `padronizar_caracteristicas()` - Garantir tamanho uniforme

**Por que é importante?**
HOG captura a forma e aparência de objetos de forma robusta.

**Teoria HOG:**
1. **Calcular gradientes**: Intensidade e direção das mudanças de pixel
2. **Células**: Dividir imagem em células (ex: 8x8 pixels)
3. **Histogramas**: Contar orientações de gradiente em cada célula
4. **Blocos**: Agrupar células e normalizar (robustez a iluminação)
5. **Concatenar**: Juntar todos os histogramas em um vetor

**Parâmetros importantes:**
- `orientations=9`: 9 bins de orientação (0-180°)
- `pixels_per_cell=(8,8)`: Células de 8x8 pixels
- `cells_per_block=(2,2)`: Blocos de 2x2 células

---

### 3. `ibus_ai/models/` - Modelos de ML

#### `svm.py` - Classificador SVM
**Conceitos aprendidos:**
- Support Vector Machine (SVM)
- Hiperplanos de separação
- Margem máxima

**Classes principais:**
- `ClassificadorPessoas` - Wrapper do SVM
- `treinar_classificador_do_zero()` - Pipeline de treinamento

**Por que é importante?**
SVM aprende a distinguir entre "pessoa" e "não-pessoa" com base nas características HOG.

**Teoria SVM:**
- Encontra o hiperplano que **maximiza a margem** entre classes
- Eficaz em espaços de alta dimensão (HOG tem centenas de dimensões)
- `LinearSVC`: Versão otimizada para classificação linear

**Parâmetros importantes:**
- `random_state=42`: Reprodutibilidade
- `max_iter=10000`: Iterações para convergência

---

### 4. `ibus_ai/infer/` - Inferência

#### `detect.py` - Detecção com Sliding Window
**Conceitos aprendidos:**
- Janela deslizante (sliding window)
- Detecção multi-escala
- Pirâmide de imagens

**Funções principais:**
- `sliding_window_deteccao()` - Pipeline de detecção
- `extrair_caixas_de_deteccoes()` - Converter formato

**Por que é importante?**
Permite detectar pessoas de diferentes tamanhos em qualquer posição da imagem.

**Teoria Sliding Window:**
1. **Definir janela**: Tamanho fixo (ex: 36x50 pixels)
2. **Deslizar**: Mover pixel por pixel (ou com passo maior)
3. **Multi-escala**: Redimensionar imagem em várias escalas
   - Escala 1.0: Pessoas grandes (próximas)
   - Escala 0.8: Pessoas médias
   - Escala 0.6: Pessoas pequenas (distantes)
4. **Classificar**: Cada janela é classificada (pessoa ou não)
5. **Mapear**: Converter coordenadas de volta para imagem original

**Parâmetros importantes:**
- `largura_janela=36, altura_janela=50`: Proporção típica de pessoa
- `tamanho_passo=8`: Passo de 8 pixels (trade-off velocidade/precisão)
- `escalas=[1.0, 0.8, 0.6]`: 3 escalas diferentes

---

### 5. `ibus_ai/utils/` - Utilitários

#### `nms.py` - Supressão Não-Máxima
**Conceitos aprendidos:**
- Overlapping detection
- IoU (Intersection over Union)
- Greedy algorithm

**Funções principais:**
- `suprimir_nao_maximos()` - Algoritmo NMS
- `aplicar_nms_em_deteccoes()` - Wrapper conveniente

**Por que é importante?**
Sliding window gera muitas detecções sobrepostas da mesma pessoa. NMS consolida em uma única detecção.

**Teoria NMS:**
1. **Ordenar**: Detecções por confiança (ou posição)
2. **Selecionar**: Pegar a de maior confiança
3. **Suprimir**: Remover detecções muito sobrepostas
4. **Repetir**: Até processar todas

**Cálculo de sobreposição (IoU):**
```
IoU = Área de Interseção / Área de União
```
- IoU = 0: Sem sobreposição
- IoU = 1: Sobreposição completa

**Parâmetros importantes:**
- `limiar_sobreposicao=0.3`: Remove caixas com >30% de IoU

---

## 🎯 Pipeline Completo (Fluxo de Dados)

```
1. IMAGEM BRUTA
   ↓
2. PRÉ-PROCESSAMENTO (256x256, cinza, normalizada)
   ↓
3. CARACTERÍSTICAS BÁSICAS (bordas, cantos, histograma)
   ↓ (apenas para visualização)
   
4. DEFINIR ROIs (anotação manual)
   ↓
5. EXTRAIR HOG DAS ROIs
   ↓
6. PADRONIZAR CARACTERÍSTICAS
   ↓
7. TREINAR SVM (pessoa vs. não-pessoa)
   ↓
   
8. NOVA IMAGEM → PRÉ-PROCESSAMENTO
   ↓
9. SLIDING WINDOW (multi-escala)
   ├─ Extrair HOG de cada janela
   ├─ Classificar com SVM
   └─ Coletar detecções positivas
   ↓
10. NMS (remover redundâncias)
   ↓
11. RESULTADO FINAL (caixas delimitadoras)
```

---

## 📖 Conceitos Teóricos Importantes

### 1. Por que Escala de Cinza?
- Reduz complexidade (1 canal vs. 3 RGB)
- Suficiente para forma/estrutura (não precisamos de cor)
- Acelera processamento

### 2. Por que Normalização (0-1)?
- Evita problemas numéricos em algoritmos
- Garante que todas as features tenham escala similar
- Facilita convergência em otimização

### 3. Por que HOG é Melhor que Bordas/Cantos?
- **Bordas**: Apenas onde há mudança (informação local)
- **Cantos**: Apenas pontos específicos
- **HOG**: Captura **padrão de gradientes** em região inteira
  - Descreve forma e textura simultaneamente
  - Robusto a pequenas variações de posição
  - Normalização por bloco → robusto a iluminação

### 4. Por que SVM?
- Eficaz com dados de alta dimensão
- Funciona bem com datasets pequenos
- Rápido para treinar e inferir
- Teoricamente bem fundamentado (margem máxima)

### 5. Por que Multi-escala?
- Pessoas aparecem em diferentes tamanhos
- Câmera fixa: pessoas próximas são grandes, distantes são pequenas
- Solução: testar mesma janela em várias escalas da imagem

### 6. Por que NMS é Necessário?
- Janela deslizante testa milhares de posições
- Mesma pessoa é detectada em várias janelas vizinhas
- Sem NMS: uma pessoa = 10+ caixas
- Com NMS: uma pessoa = 1 caixa

---

## 🧪 Experimentos para Aprender

### Experimento 1: Efeito dos Parâmetros Canny
```python
# Testar diferentes limiares
bordas1 = detectar_bordas_canny(imagem, limiar1=30, limiar2=100)
bordas2 = detectar_bordas_canny(imagem, limiar1=50, limiar2=150)
bordas3 = detectar_bordas_canny(imagem, limiar1=100, limiar2=200)
```
**O que observar:** Limiares altos = menos bordas (apenas as mais fortes)

---

### Experimento 2: Efeito do Tamanho da Célula HOG
```python
# Células pequenas vs. grandes
hog1 = extrair_hog(patch, pixels_por_celula=(4, 4))   # Mais detalhes
hog2 = extrair_hog(patch, pixels_por_celula=(8, 8))   # Padrão
hog3 = extrair_hog(patch, pixels_por_celula=(16, 16)) # Mais geral
```
**O que observar:** Células pequenas capturam mais detalhes mas são mais sensíveis a ruído

---

### Experimento 3: Efeito do Limiar NMS
```python
# NMS agressivo vs. permissivo
caixas1 = aplicar_nms_em_deteccoes(deteccoes, limiar=0.1)  # Muito agressivo
caixas2 = aplicar_nms_em_deteccoes(deteccoes, limiar=0.3)  # Padrão
caixas3 = aplicar_nms_em_deteccoes(deteccoes, limiar=0.5)  # Permissivo
```
**O que observar:** Limiar baixo remove mais caixas, limiar alto permite mais sobreposição

---

### Experimento 4: Efeito do Tamanho do Passo
```python
# Passo pequeno vs. grande no sliding window
deteccoes1 = sliding_window_deteccao(..., tamanho_passo=4)   # Lento, preciso
deteccoes2 = sliding_window_deteccao(..., tamanho_passo=8)   # Balanceado
deteccoes3 = sliding_window_deteccao(..., tamanho_passo=16)  # Rápido, impreciso
```
**O que observar:** Passo pequeno testa mais posições (mais preciso mas mais lento)

---

## ❓ Perguntas para Reflexão

1. **Por que não usar apenas cores para detectar pessoas?**
   - R: Roupas têm cores muito variadas, fundo também

2. **Por que normalizar características antes do SVM?**
   - R: Features com escalas diferentes podem dominar a decisão

3. **O que acontece se treinarmos com apenas exemplos positivos?**
   - R: Modelo detectaria tudo como pessoa (sem exemplos negativos para contrastar)

4. **Por que não testar todas as escalas possíveis?**
   - R: Custo computacional seria proibitivo

5. **Como escolher o limiar de sobreposição do NMS?**
   - R: Trade-off entre remover redundâncias e manter detecções válidas próximas

---

## 🚀 Próximos Passos de Estudo

### Nível Iniciante
- [x] Entender cada módulo individualmente
- [x] Rodar o pipeline completo
- [ ] Testar com suas próprias imagens
- [ ] Modificar parâmetros e observar efeitos

### Nível Intermediário
- [ ] Implementar outras características (LBP, SIFT)
- [ ] Tentar outros classificadores (Random Forest, KNN)
- [ ] Coletar dataset próprio e anotar
- [ ] Implementar métricas de avaliação (Precision, Recall)

### Nível Avançado
- [ ] Estudar YOLO (detecção com deep learning)
- [ ] Implementar data augmentation
- [ ] Treinar rede neural convolucional
- [ ] Implementar tracking de pessoas em vídeo

---

## 📚 Recursos de Estudo Adicionais

### Livros
- "Computer Vision: Algorithms and Applications" - Richard Szeliski
- "Pattern Recognition and Machine Learning" - Christopher Bishop

### Cursos Online
- CS231n (Stanford) - Convolutional Neural Networks
- Udacity - Computer Vision Nanodegree

### Papers Importantes
- "Histograms of Oriented Gradients for Human Detection" (Dalal & Triggs, 2005)
- "Support-Vector Networks" (Cortes & Vapnik, 1995)

---

## 💡 Dicas de Estudo

1. **Não pule etapas**: Entenda cada função antes de prosseguir
2. **Visualize tudo**: Use as funções de visualização para "ver" o que acontece
3. **Experimente**: Mude parâmetros e observe os efeitos
4. **Documente**: Anote suas descobertas e dúvidas
5. **Compre**: Com implementações de deep learning modernas

**Boa sorte nos estudos! 🎓**
