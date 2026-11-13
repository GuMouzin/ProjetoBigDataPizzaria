import pandas as pd

# Lê o arquivo original pesado
df = pd.read_csv('dados_parte1.csv')

# Pega apenas as primeiras 1000 linhas
sample_df = df.head(1000)

# Salva a versão leve
sample_df.to_csv('dados_parte1_sample.csv', index=False)
