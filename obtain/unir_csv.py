import pandas as pd
import glob

def unzipfolder(path, output):
	files = glob.glob(path + "\\*.zip")
	print(f"Leyendo {len(files)} archivos...")
	l = [pd.read_csv(filename) for filename in files]
	print("Concatenando...")
	df = pd.concat(l, axis=0)
	print("Exportando...")
	df.to_csv(path + "\\" + output)

"""
l = [filename for filename in glob.glob(path + "\\*.zip")]
print(path + "\\*.zip")
print(*l, sep = "\n")
"""

path = r"C:\Users\juanc\Google Drive\DS4All_Team28\Listado Estaciones IDEAM 1990-2020\data"
output = "est_limnimetrica.csv"
#TEST

print(f"Directorio:{path}")
print(f"Salida:{output}")
unzipfolder(path, output)

#df = pd.read_csv(path + output)
#print(df.shape)

