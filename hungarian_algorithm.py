import sys
import re
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

WEIGHTS = {
    "X": 1.0,  # Regras
    "Y": 1.0,  # Lealdade
    "Z": 1.0,  # Atuação
}


def carregar_dados(caminho_csv: str) -> pd.DataFrame:
    df = pd.read_csv(caminho_csv)
    df.columns = df.columns.str.strip()

    if "extra_info" in df.columns:
        df = df.drop(columns=["extra_info"])

    colunas_esperadas = {"nome", "X", "Y", "Z"}
    if not colunas_esperadas.issubset(df.columns):
        raise ValueError(
            f"O arquivo {caminho_csv} precisa ter as colunas: {colunas_esperadas}. "
            f"Colunas encontradas: {list(df.columns)}"
        )
    return df


def montar_matriz_de_custo(participantes: pd.DataFrame, delegados: pd.DataFrame) -> np.ndarray:
    """
    Constrói a matriz N x M de distâncias euclidianas ponderadas entre
    cada participante (linha) e cada delegado (coluna).
    """
    p_coords = participantes[["X", "Y", "Z"]].to_numpy(dtype=float)
    d_coords = delegados[["X", "Y", "Z"]].to_numpy(dtype=float)

    w = np.array([WEIGHTS["X"], WEIGHTS["Y"], WEIGHTS["Z"]])

    # Distância euclidiana ponderada entre cada par
    diff = p_coords[:, np.newaxis, :] - d_coords[np.newaxis, :, :]
    dist_sq_ponderada = np.sum((diff ** 2) * w, axis=2)
    return np.sqrt(dist_sq_ponderada)


def alocar(participantes: pd.DataFrame, delegados: pd.DataFrame) -> pd.DataFrame:
    n_part, n_deleg = len(participantes), len(delegados)

    if n_part != n_deleg:
        print(
            f"[AVISO] Número de participantes ({n_part}) difere do número de "
            f"delegados ({n_deleg}). O algoritmo ainda funciona (ele resolve "
            f"o maior subconjunto possível), mas sobrarão "
            f"{abs(n_part - n_deleg)} pessoas ou vagas sem par.\n"
        )

    custo = montar_matriz_de_custo(participantes, delegados)

    linhas, colunas = linear_sum_assignment(custo)

    resultados = []
    relatorio = []
    for i, j in zip(linhas, colunas):
        relatorio.append(
            {
                "participante": re.sub(r'[^\w\s]', '', participantes.iloc[i]["nome"].strip()),
                "delegado": delegados.iloc[j]["nome"],
                "distancia": round(float(custo[i, j]), 3),
                "participante_X": round(participantes.iloc[i]["X"], 3),
                "participante_Y": round(participantes.iloc[i]["Y"], 3),
                "participante_Z": round(participantes.iloc[i]["Z"], 3),
                "delegado_X": delegados.iloc[j]["X"],
                "delegado_Y": delegados.iloc[j]["Y"],
                "delegado_Z": delegados.iloc[j]["Z"],
            }
        )
        resultados.append(
            {
                "participante": re.sub(r'[^\w\s]', '', participantes.iloc[i]["nome"].strip()),
                "delegado": delegados.iloc[j]["nome"],
                "distancia": round(float(custo[i, j]), 3)
            }
        )

    resultado_df = pd.DataFrame(resultados).sort_values("distancia").reset_index(drop=True)
    relatorio_df = pd.DataFrame(relatorio).sort_values("distancia").reset_index(drop=True)
    return resultado_df, relatorio_df


def main():
    if len(sys.argv) != 2:
        print("Uso: python hungarian_algorithm.py data/participantes.csv ")
        sys.exit(1)

    caminho_participantes, caminho_delegados = sys.argv[1], 'data/delegados.csv'

    participantes = carregar_dados(caminho_participantes)
    delegados = carregar_dados(caminho_delegados)

    resultado, relatorio = alocar(participantes, delegados)

    print("\n=== ALOCAÇÃO ÓTIMA (menor soma total de distâncias) ===\n")
    print(resultado.to_string(index=False))

    custo_total = resultado["distancia"].sum()
    custo_medio = resultado['distancia'].mean()
    print(f"\nCusto total (soma das distâncias): {custo_total:.3f}")
    print(f"Distância média por match: {custo_medio:.3f}")

    resultado_bruto = resultado.drop(columns=["distancia"])

    saida = "final_result/alocacao_final.csv"
    path_relatorio = "final_result/relatorio.csv"
    resultado_bruto.to_csv(saida, index=False)
    relatorio.to_csv(path_relatorio, index=False)
    print(f"\nResultados salvos em: {saida}")


if __name__ == "__main__":
    main()