import pandas as pd

df = pd.read_csv('C:/Users/23300037/Downloads/Projeto_Museu_PA_Emilio_Goeldi/tabela.csv', sep=';')
df01 = df[['gbifID', 'recordedBy']]
f = open('pesquisador.csv', 'w')

print(df01)

for row in df01.index:
    f.write(f"INSERT INTO pesquisador (recorded_by, gbifID) VALUES ('{df01['recordedBy'][row]}', {df01['gbifID'][row]});\n")
