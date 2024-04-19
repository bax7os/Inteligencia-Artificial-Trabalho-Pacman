## Trabalho de Inteligência Artificial.

Objetivo: Implementar o Minimax e suas variações. 

- Poda Alfa-Beta 
- Expectimax

- Extra: Best_Action baseada na quantidade de comidas, ghosts e capsulas próximas ao agente 1 (Pacman).



## Comandos

#### Minimax

```http
  python pacman.py -p MinimaxAgent -a depth=3
```

#### Poda Alfa-Beta

```http
  python pacman.py -p AlphaBetaAgent -a depth=3
```
#### Expectimax

```http
    python pacman.py -p ExpectimaxAgent -a depth=3
```

### betterEvoluctionFunction

Para testar a sua nova função, altere a função como
seguinte:
```http
    def scoreEvaluationFunction(currentGameState):
        #return currentGameState.getScore()
        return betterEvaluationFunction(currentGameState)
```


## Referência

 - [The Pac-man Projects](http://ai.berkeley.edu/project_overview.html)
 - [Baseado em](https://github.com/khanhngg/CSC665-multi-agent-pacman/blob/master/multiagent/multiAgents.py)


