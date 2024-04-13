import pandas as pd
import wget
import os

def leer_csv(path: str) -> pd.DataFrame:
    
    url='https://www.football-data.co.uk/mmz4281/0809/SP1.csv' #2223 es el año de la liga
    wget.download(url, path)
    print('Datos Descargados!')
    
    dataframe_datos_partidos = pd.read_csv(path)
    return dataframe_datos_partidos

def formatear_datos(dataframe: pd.DataFrame, path: str):
    columnas = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','HTHG','HTAG','HS','AS','HST','AST','HY','AY','HR','AR','FTR']
    dataframe_datos_formateados = dataframe[columnas]
    dataframe_datos_formateados.to_csv(path, index=False)
    
if __name__ == "__main__":
    CARPETA_DATOS_PUROS = "C:/Users/User/OneDrive/Escritorio/Cosas_TFG/Futbol/Datos_Puros/"
    CARPETA_DATOS_FORMATEADOS = "C:/Users/User/OneDrive/Escritorio/Cosas_TFG/Futbol/Datos_Formateados/"
    #archivos = os.listdir(CARPETA_DATOS_PUROS)
    #for archivo in archivos:
    dataframe = leer_csv(CARPETA_DATOS_PUROS+'SP1-0809.csv')
    formatear_datos(dataframe=dataframe, path=CARPETA_DATOS_FORMATEADOS+'SP1-0809.csv')