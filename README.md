# Alocação de Delegados — Comitê Ad Hoc Watergate
 
Ferramenta para alocar de maneira determinística participantes de uma simulação da ONU a perfis de
delegado, com base em três eixos de perfil comportamental, garantindo o
melhor encaixe geral e sem repetições.
 
## O problema
 
Cada participante e cada delegado são mapeados em três eixos, numa escala
de 1 a 5:
 
| Eixo | 1 | 5 |
|---|---|---|
| **X — Regras** | Legalista / Institucional | Pragmático / Guerra Assimétrica |
| **Y — Lealdade** | Autopreservação / Delação | Lealdade / Blindagem |
| **Z — Atuação** | Bastidores / Sombras | Holofotes / Protagonismo Público |
 
O objetivo é casar cada participante com um delegado diferente, minimizando
a distância total de perfil entre todos os pares, ou seja, o melhor encaixe
do grupo como um todo.
 
## Método
 
Isso é um **problema de atribuição (assignment problem)**, resolvido de
forma exata pelo **Algoritmo Húngaro (Kuhn-Munkres)**, via
`scipy.optimize.linear_sum_assignment`.
 
A distância entre um participante `i` e um delegado `j` é a distância
euclidiana (opcionalmente ponderada) no espaço (X, Y, Z):
 
$$
d(i,j) = \sqrt{w_X*(X_i-X_j)² + w_Y*(Y_i-Y_j)² + w_Z*(Z_i-Z_j)²}
$$

## Formato dos CSVs de entrada
 
Tanto `data/participantes.csv` quanto `data/delegados.csv` devem ter as colunas:
 
```csv
nome,X,Y,Z
Ana Silva,4,2,5
Bruno Costa,1,5,1
```
 
- `nome`: identificação da pessoa/delegado.
- `X`, `Y`, `Z`: notas de 1 a 5 nos três eixos descritos.
 
## Como usar
 
### 1. Gerar dados de amostra (opcional, para testes)
 
```bash
python gerar_amostras.py
```
 
### 2. Rodar a alocação
 
```bash
python alocar_delegados.py data/participantes.csv data/delegados.csv
```

O nome do arquivo de entrada, tanto de delegados, quanto de participantes pode variar.
 
Saída no terminal:
 
- Tabela com o match de cada participante, o delegado atribuído e a
  distância de perfil entre os dois.
- Custo total (soma de todas as distâncias) e distância média por match.
Além disso, o resultado é salvo em `alocacao_resultado.csv`.
 
## Ajustando pesos dos eixos
 
Se algum eixo deve pesar, edite o dicionário `WEIGHTS` no topo de
`alocar_delegados.py`:
 
```python
WEIGHTS = {
    "X": 1.0,  # Regras
    "Y": 1.0,  # Lealdade
    "Z": 1.0,  # Atuação
}
```
 
Aumentar o peso de um eixo (ex.: `"Y": 2.0`) faz diferenças nesse eixo
pesarem mais no cálculo da distância total.
 
## Observação
 
- O número de participantes e de delegados deve ser igual para que a
  alocação seja 1-para-1 completa. Se houver diferença, o script avisa e
  resolve o maior encaixe possível, mas sobrará gente ou vaga sem par.