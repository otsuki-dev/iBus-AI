""""""

Classificador SVM (Support Vector Machine)Módulo de Classificador SVM

Funções para treinar e usar classificador SVM para detecção de pessoas

Implementação de classificador para detecção de pessoas usando SVM com kernel linear."""

"""

import numpy as np

import numpy as npfrom sklearn.svm import LinearSVC

from sklearn.svm import LinearSVC

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import pickleclass ClassificadorPessoas:

    """

    Classificador para distinguir entre 'pessoa' e 'não-pessoa'

class ClassificadorPessoas:    usando características HOG e SVM Linear.

    """    """

    Wrapper para classificador SVM de detecção de pessoas.    

    """    def __init__(self, estado_aleatorio=42, max_iter=10000):

            """

    def __init__(self, C=1.0, max_iter=10000):        Inicializa o classificador.

        """        

        Inicializa o classificador.        Args:

                    estado_aleatorio: Seed para reprodutibilidade

        Args:            max_iter: Número máximo de iterações para convergência

            C (float): Parâmetro de regularização        """

            max_iter (int): Número máximo de iterações        self.classificador = LinearSVC(

        """            random_state=estado_aleatorio,

        self.modelo = LinearSVC(C=C, max_iter=max_iter, random_state=42)            max_iter=max_iter

        self.treinado = False        )

        self.estatisticas_norm = None  # (média, desvio) para normalização        self.treinado = False

                self.comprimento_caracteristicas = None

    def treinar(self, X_train, y_train):    

        """    def treinar(self, X, y):

        Treina o classificador.        """

                Treina o classificador com características e rótulos.

        Args:        

            X_train (numpy.ndarray): Características de treino        Args:

            y_train (numpy.ndarray): Labels de treino (1 = pessoa, 0 = não-pessoa)            X: Array numpy 2D de características (amostras x características)

        """            y: Array numpy 1D de rótulos ('person' ou 'non-person')

        self.modelo.fit(X_train, y_train)        """

        self.treinado = True        self.classificador.fit(X, y)

                self.treinado = True

    def predizer(self, X):        self.comprimento_caracteristicas = X.shape[1]

        """        

        Faz predições para novos dados.        print("Classificador treinado com sucesso!")

                print(f"Formato das características (X): {X.shape}")

        Args:        print(f"Formato dos rótulos (y): {y.shape}")

            X (numpy.ndarray): Características para predição    

                def prever(self, X):

        Returns:        """

            numpy.ndarray: Predições (1 = pessoa, 0 = não-pessoa)        Faz previsões para novas amostras.

        """        

        if not self.treinado:        Args:

            raise ValueError("Modelo não foi treinado ainda!")            X: Array numpy de características (1D ou 2D)

        return self.modelo.predict(X)            

            Returns:

    def predizer_proba(self, X):            Predições ('person' ou 'non-person')

        """        """

        Retorna scores de confiança das predições.        if not self.treinado:

                    raise ValueError("Classificador precisa ser treinado antes de fazer previsões")

        Args:        

            X (numpy.ndarray): Características para predição        # Garantir que X seja 2D

                    if len(X.shape) == 1:

        Returns:            X = X.reshape(1, -1)

            numpy.ndarray: Scores de decisão        

        """        return self.classificador.predict(X)

        if not self.treinado:    

            raise ValueError("Modelo não foi treinado ainda!")    def prever_prob(self, X):

        return self.modelo.decision_function(X)        """

            Retorna scores de decisão (confiança) para previsões.

    def salvar(self, caminho):        

        """        Args:

        Salva o modelo treinado.            X: Array numpy de características

                    

        Args:        Returns:

            caminho (str): Caminho para salvar o modelo            Scores de decisão

        """        """

        if not self.treinado:        if not self.treinado:

            raise ValueError("Modelo não foi treinado ainda!")            raise ValueError("Classificador precisa ser treinado antes de fazer previsões")

                

        dados = {        if len(X.shape) == 1:

            'modelo': self.modelo,            X = X.reshape(1, -1)

            'estatisticas_norm': self.estatisticas_norm        

        }        return self.classificador.decision_function(X)

        

        with open(caminho, 'wb') as f:

            pickle.dump(dados, f)def treinar_classificador_do_zero(lista_caracteristicas, lista_rotulos):

        """

    @classmethod    Treina um classificador do zero com características HOG.

    def carregar(cls, caminho):    

        """    Args:

        Carrega um modelo salvo.        lista_caracteristicas: Lista de arrays de características HOG

                lista_rotulos: Lista de rótulos correspondentes

        Args:        

            caminho (str): Caminho do modelo salvo    Returns:

                    Tupla (classificador treinado, comprimento máximo de características)

        Returns:    """

            ClassificadorPessoas: Classificador carregado    from ..features.hog import padronizar_caracteristicas

        """    

        with open(caminho, 'rb') as f:    # Padronizar características para comprimento uniforme

            dados = pickle.load(f)    X, comprimento_max = padronizar_caracteristicas(lista_caracteristicas)

            

        classificador = cls()    # Converter rótulos para array numpy

        classificador.modelo = dados['modelo']    y = np.array(lista_rotulos)

        classificador.estatisticas_norm = dados.get('estatisticas_norm')    

        classificador.treinado = True    # Criar e treinar classificador

            classificador = ClassificadorPessoas()

        return classificador    classificador.treinar(X, y)

    

    return classificador, comprimento_max

def treinar_classificador_do_zero(X_positivos, X_negativos, C=1.0, verbose=True):
    """
    Treina um classificador do zero com exemplos positivos e negativos.
    
    Args:
        X_positivos (numpy.ndarray): Características de exemplos positivos (pessoas)
        X_negativos (numpy.ndarray): Características de exemplos negativos (não-pessoas)
        C (float): Parâmetro de regularização do SVM
        verbose (bool): Se True, exibe informações do treinamento
        
    Returns:
        ClassificadorPessoas: Classificador treinado
    """
    # Combinar dados
    X_train = np.vstack([X_positivos, X_negativos])
    y_train = np.array([1] * len(X_positivos) + [0] * len(X_negativos))
    
    if verbose:
        print(f"📊 Dataset de treino:")
        print(f"  - Exemplos positivos (pessoas): {len(X_positivos)}")
        print(f"  - Exemplos negativos (não-pessoas): {len(X_negativos)}")
        print(f"  - Total: {len(X_train)}")
        print(f"  - Dimensão das features: {X_train.shape[1]}")
    
    # Criar e treinar classificador
    classificador = ClassificadorPessoas(C=C)
    
    if verbose:
        print("\n🔧 Treinando classificador SVM...")
    
    classificador.treinar(X_train, y_train)
    
    if verbose:
        print("✅ Treinamento concluído!")
        
        # Avaliar no próprio treino (como baseline)
        y_pred = classificador.predizer(X_train)
        acuracia = accuracy_score(y_train, y_pred)
        print(f"\n📈 Acurácia no treino: {acuracia:.2%}")
    
    return classificador


def avaliar_classificador(classificador, X_test, y_test, verbose=True):
    """
    Avalia o desempenho de um classificador.
    
    Args:
        classificador (ClassificadorPessoas): Classificador treinado
        X_test (numpy.ndarray): Características de teste
        y_test (numpy.ndarray): Labels verdadeiros
        verbose (bool): Se True, exibe métricas detalhadas
        
    Returns:
        dict: Dicionário com métricas de avaliação
    """
    y_pred = classificador.predizer(X_test)
    
    metricas = {
        'acuracia': accuracy_score(y_test, y_pred),
        'precisao': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1': f1_score(y_test, y_pred, zero_division=0)
    }
    
    if verbose:
        print("📊 Métricas de Avaliação:")
        print(f"  - Acurácia:  {metricas['acuracia']:.2%}")
        print(f"  - Precisão:  {metricas['precisao']:.2%}")
        print(f"  - Recall:    {metricas['recall']:.2%}")
        print(f"  - F1-Score:  {metricas['f1']:.2%}")
    
    return metricas
