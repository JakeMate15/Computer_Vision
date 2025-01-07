import os
import pandas as pd

df = pd.read_csv('dataset.csv')
print(df.columns)
df['imagen'] = df['imagen'].str.strip()
df = df.drop_duplicates(subset='imagen')
df.to_csv('dataset.csv', index=False)

# directorio = './'
# archivos = [f for f in os.listdir(directorio) if f.endswith('csv')]

# dfs = []

# for archivo in archivos:
#     ruta = os.path.join(directorio, archivo)
#     df = pd.read_csv(ruta)
#     dfs.append(df)

# df_final = pd.concat(dfs)
# df_final = df_final.drop_duplicates()

# prim = df_final.columns[0]
# df_final = df_final.sort_values(by=prim)
# df_final.to_csv('dataset.csv', index=False)
