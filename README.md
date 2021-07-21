# Python API para Algo Trading

Esse repositório tem por objetivo hospedar os servidores referentes a Roteamento e Market Data, fornecidos pelo MetaTrader 5.

## Estrutura do Repositório

A estrutura abordada dentro do projeto de API é o seguinte

```
src
    |- charts
        |- chart.py
    |- database
        |- ohlc
        |- ticks
    |- models
        |- model_name.py
    |- servers
        |- server_mt5.py
    |- setups

tests
    |- models
        |- test_models.py
    |- server
        |- test_server.py
```

Entrando em detalhes em cada pasta temos:

---
* `src` pasta padrão do repositório referente a todo o código da API.
* `src/charts` referente a construção de gráficos personalizados para o python (somente a representação Dataframe, não temos implementado a visualização do gráfico em MetaTrader5).
* `src/database` referente a todos os dados utilizados para o treinamento dos modelos e criação de gráficos personalizados.
* `src/models` pasta que armazena todas as classes de modelos de Inteligência Artificial. Todos os modelos apresentam um Pipeline para a execução de treinamento e predição.
* `src/server` pasta que tem por objetivo armazenar toda a regra de negócio da API de comunicação com o Python e o MetaTrader5.
* `src/setups` referente a toda a lógica de operação das estratégias para algo trading.
---
* `test` pasta padrão do repositório referente a todo o código de testes para a API.
* `test/models` referente ao código de testes dos modelos de Inteligência Artificial.
* `test/server` referente ao código de testes da regra de negócio dos servidores da API.

## Modelos de Inteligência Artificial



## Dependências

Para instalar as dependências do repositório execute o seguinte comando:

`pip install -r requirements.txt`


