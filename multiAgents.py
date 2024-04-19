# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
#
# Inteligêcia Artificial - Prof. Wesley Nunes
# Ana Clara Bastos Moraes - 202219040523
# 
#

from util import manhattanDistance
from game import Directions
import random, util
from pacman import GameState
from game import Agent

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    #return currentGameState.getScore()
    return betterEvaluationFunction(currentGameState)
class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """
        # Inicializa a melhor ação como None e o melhor valor como -infinito
        best_action = None
        best_value = float('-inf')
        
        # Obtém todas as ações legais para o Pacman
        legal_actions = gameState.getLegalActions(0)

        # Itera sobre todas as ações legais possiveis
        for action in legal_actions:
            # Gera o estado sucessor após o Pacman tomar uma ação
            successor = gameState.generateSuccessor(0, action)
            # Calcula o valor minimax do estado sucessor
            value = self.minimax(successor, 1, self.depth)
            # Se o valor calculado é melhor que o melhor valor atual, atualiza a melhor ação e o melhor valor
            if value > best_value:
                best_value = value
                best_action = action

        # Retorna a melhor ação
        return best_action





    def minimax(self, gameState: GameState, agent_index, depth):
        
        # Condição de parada na chamada recursiva
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        

        # Responsável pelo MAX --> pacman
        if agent_index == 0:         # MAX
            bestValueMax = float('-inf')

            # Pega todas as jogadas legais possíveis no estado de jogo
            jogadas = gameState.getLegalActions(agent_index)


            for action in jogadas:
                # Gera os sucessores
                futureAction = gameState.generateSuccessor(agent_index, action)
                value = MinimaxAgent.minimax(self, futureAction, 1, depth)

                # Atualiza o melhor valor baseado nas ações futuras geradas
                if value > bestValueMax:
                    bestValueMax = value
            
            # Retorna o valor MAX
            return bestValueMax
        

        # Responsável pelo MIN --> ghosts
        else: # MIN      
            
            # Atualiza o agente
            nextAgent = agent_index + 1 
            bestValueMin = float('+inf')

            if gameState.getNumAgents() == nextAgent: 
                nextAgent = 0
                depth -= 1
            

            jogadas = gameState.getLegalActions(nextAgent)
            for action in jogadas:
                futureAction = gameState.generateSuccessor(nextAgent, action)
                value = MinimaxAgent.minimax(self, futureAction, nextAgent, depth)
                # Atualiza o melhor valor do MIN
                if value < bestValueMin:
                    bestValueMin = value

            # Retorna o valor MIN
            return bestValueMin

    




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
         # Inicializa a melhor ação como None e o melhor valor como -infinito
        
        best_action = None
        best_value = float('-inf')
        alfa = float('-inf')
        beta = float('+inf')
        # Obtém todas as ações legais para o Pacman
        legal_actions = gameState.getLegalActions(0)

        # Itera sobre todas as ações legais
        for action in legal_actions:
            # Gera o estado sucessor após o Pacman tomar uma ação
            successor = gameState.generateSuccessor(0, action)
            # Calcula o valor minimax do estado sucessor
            value = self.alfabeta(successor, 1, self.depth, alfa, beta)
            # Se o valor calculado é melhor que o melhor valor atual, atualiza a melhor ação e o melhor valor
            if value > best_value:
                best_value = value
                best_action = action

        # Retorna a melhor ação
        return best_action
    

    def alfabeta(self, gameState: GameState, agent_index, depth, alfa, beta):

        # Condição de parada da chamada recursiva
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        
        
        if agent_index == 0:         # MAX
            value = float('-inf')
            jogadas = gameState.getLegalActions(agent_index)

            for action in jogadas:
                futureAction = gameState.generateSuccessor(agent_index, action)

                # Atualiza o valor do melhor estado encontrado
                value = max(value, self.alfabeta(futureAction, 1, depth, alfa, beta))
                
                # Realiza a poda quando acha um valor maior do que o beta
                if value > beta:
                    return value
                # Atualiza o valor do alfa
                alfa = max(alfa, value)


            return value

        else:      # MIN

            # Atualiza o agente
            nextAgent = agent_index + 1                 
            if gameState.getNumAgents() == nextAgent: 
                nextAgent = 0
                depth -= 1

            
            value = float('inf')
            jogadas = gameState.getLegalActions(nextAgent)


            for action in jogadas:
                futureAction = gameState.generateSuccessor(nextAgent, action)

                # Atualiza o valor do melhor estado encontrado
                value = min(value, self.alfabeta(futureAction, nextAgent, depth, alfa, beta))

                # Realiza a poda quando acha um valor menor do que o alfa 
                if value < alfa:
                    return value
                
                # Atualiza o beta
                beta = min(beta, value)

            return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # Inicialização chamando o expectimax com o estado atual do jogo
        expectimax = self.expectimax(depth=self.depth, gameState=gameState, agent_index=0)


        return expectimax[1]

    def expectimax(self, depth, gameState: GameState, agent_index):


        # Condição de parada para a chamada recursiva
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None
        


        if agent_index == 0: # MAX

            bestValue = float("-inf")
            bestAction = None
            jogadas = gameState.getLegalActions(agent_index)

            # Neste loop é retornado o melhor valor e melhor ação para o pacman, baseado na
            # chamda recursiva ao expectimax, que fará uma análise a partir da média entre os ultimos sucessores.
            for action in jogadas:
                futureAction = gameState.generateSuccessor(agent_index, action)
                value, _ = self.expectimax(depth, futureAction, 1)
                if value > bestValue:
                    bestValue = value
                    #print("MELHOR VALOR")
                    #print(bestValue)
                    bestAction = action
                    #print("MELHOR acao")
                    #print( bestAction)
            return bestValue, bestAction
        
        else: # MIN

            value = 0
            nextAgent = agent_index + 1
            if gameState.getNumAgents() == nextAgent: 
                nextAgent = 0
                depth -= 1
            jogadas = gameState.getLegalActions(agent_index)
            
            # Neste loop é retornado a média entre os valores dos estados sucessores, isso depois
            # de ter examinado todas as ações. 
            for action in jogadas:
                futureAction = gameState.generateSuccessor(agent_index, action)
                value += self.expectimax(depth, futureAction, nextAgent)[0]
                #print("VALOR")
                #print(value)
            return value / len(gameState.getLegalActions(agent_index)), None



def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    #POSIÇÕES E PONTUAÇÃO
    #Pegandos a posição atual do pacman e dos ghosts, assim como a pontuação atual do jogo.

    pontuacao = currentGameState.getScore()
    posicao_pacman = currentGameState.getPacmanPosition()
    quantidade_ghosts = currentGameState.getNumAgents() - 1 # Tira -1 pois o pacman não está incluso
    for i in range(1, quantidade_ghosts+1):
        posicao_ghosts = [currentGameState.getGhostPosition(i)]


    #QUANTIDADE DE COMIDAS E CAPSULAS
    #Colocando em lista a posição da comida e sua quantidade, assim como as capsulas, que são os pontos maiores.
    comidas_list = currentGameState.getFood().asList()
    quantidade_comidas = len(comidas_list)
    contador_capsulas = len(currentGameState.getCapsules())
    capsulas_list = currentGameState.getCapsules()
    comidas_perto = 1
    capsulas_perto = 1

        #Utilizei o metódo manhattan para encontrar a distância entre a posição atual do pacman e as comidas e capsulas
    for posicao_comida in comidas_list:
        distancia_comidas = [manhattanDistance(posicao_pacman, posicao_comida)]
   

    for posicao_capsula in capsulas_list:
        distancia_capsulas = [manhattanDistance(posicao_pacman, posicao_capsula)]
    

    
    # Se ainda houver comidas ou capsulas disponíveis, guardar a menor distância entre o pacman e esse item
    if contador_capsulas > 0:
        capsulas_perto = min(distancia_capsulas)

    if quantidade_comidas > 0:
        comidas_perto = min(distancia_comidas)

    # Nesse loop, analisamos a distância do pacman em relação aos ghosts.
    # Se o ghost estiver muito próximo do pacman, ele prioriza escapar do que comer a comida/capsula mais próxima. 
    # Por isso, resetamos o valor da distancia da comida/capsula mais próxima para um número alto.
    for ghosts in posicao_ghosts:
        distancia_ghosts = manhattanDistance(posicao_pacman, ghosts)

        if distancia_ghosts < 3:
           comidas_perto = 10000
           capsulas_perto = 10000



    # Guardando em uma lista a combinação de todos os dados obtidos.
    # O 1 / comidas_perto nos dá que quanto mais próximo o pacman estiver de uma comida, maior será esse valor. 
    # Assim acontece tabém com as capsulas.
    combinacao = [1 / comidas_perto, pontuacao, quantidade_comidas, contador_capsulas, 1 / capsulas_perto]

    # Esses são os pesos designados para cada ítem da lista combinação. 

    pesos = [20, 300, -150, -15, 30]
    
    # Combinando os pesos com suas características, multiplicando eles entre si.
    soma = []

    for combinacao, pesos in zip(combinacao, pesos):
        soma.append(combinacao*pesos) 

    new_result = sum(soma)
    

    return new_result















   
    
    
    
    
    
    
    
    
    
    
    
# Abbreviation
better = betterEvaluationFunction
