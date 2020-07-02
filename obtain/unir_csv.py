import pandas as pd
import glob

def unzipfolder(path, output):
	files = glob.glob(path)
	print(f"Leyendo {len(files)} archivos...")
	l = [pd.read_csv(filename) for filename in files]
	print("Concatenando...")
	df = pd.concat(l, axis=0)
#	df.drop(["i"], axis="columns", inplace = True)
	
#	df.drop_duplicates('codigo', inplace = True)
    
	print("Exportando...")
	df.to_csv(output,  index = False)

"""
l = [filename for filename in glob.glob(path + "\\*.zip")]
print(path + "\\*.zip")
print(*l, sep = "\n")
"""

path = r"C:\Users\juanc\Source\Repos\DS4All_2020_Team28_Project\data\variables_profiles\CUM70_*.csv"
output = r"C:\Users\juanc\Source\Repos\DS4All_2020_Team28_Project\data\variables_profiles\CUM70_todas.csv"
#TEST

print(f"Directorio:{path}")
print(f"Salida:{output}")
unzipfolder(path, output)

#df = pd.read_csv(path + output)
#print(df.shape)

