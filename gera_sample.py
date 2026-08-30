import pandas as pd
import numpy as np
import random

# Gerando nomes aleatórios
nomes = ["Ana", "Bruno", "Carlos", "Diana", "Eduardo", "Fernanda", "Gabriel", "Helena"]
sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Almeida", "Costa"]

nomes_completos = []

while len(nomes_completos) < 20:
    nome = random.choice(nomes)
    sobrenome = random.choice(sobrenomes)
    nc = f"{nome} {sobrenome}"

    if nc not in nomes_completos:
        nomes_completos.append(nc)

# Gerando valores aleatórios pros eixos
np.random.seed(42)

rng = np.random.default_rng()

array_1 = rng.uniform(1.0, 5.0, size=20)
array_2 = rng.uniform(1.0, 5.0, size=20)
array_3 = rng.uniform(1.0, 5.0, size=20)

df = pd.DataFrame({
    'nome': nomes_completos,
    'X': array_1,
    'Y': array_2,
    'Z': array_3,
})

df.to_csv(".data/participantes.csv", index=False)