import pandas as pd
import wget
import os

def leer_csv(path: str, year: int) -> pd.DataFrame:
    if os.path.exists(path):
        os.remove(path)
    url='https://www.football-data.co.uk/mmz4281/'+year+'/SC0.csv' #2223 es el año de la liga
    wget.download(url, path)
    print('Datos Descargados!')
    
    dataframe_datos_partidos = pd.read_csv(path)
    return dataframe_datos_partidos

def formatear_datos(dataframe: pd.DataFrame, path: str):
    columnas = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','HTHG','HTAG','HS','AS','HST','AST','HY','AY','HR','AR','FTR']
    dataframe_datos_formateados = dataframe[columnas]
    if os.path.exists(path):
        os.remove(path)
    dataframe_datos_formateados.to_csv(path, index=False)
    
if __name__ == "__main__":
    years = ['1011','1112','1213','1314','1415','1516','1617','1718','1819','1920','2021','2122','2223','2324',]
    CARPETA_DATOS_PUROS = "C:/Users/User/OneDrive/Escritorio/Cosas_TFG/Futbol/Datos_Puros/"
    CARPETA_DATOS_FORMATEADOS = "C:/Users/User/OneDrive/Escritorio/Cosas_TFG/Futbol/Datos_Formateados/"
    #archivos = os.listdir(CARPETA_DATOS_PUROS)
    #for archivo in archivos:
    for year in years:
        dataframe = leer_csv(CARPETA_DATOS_PUROS+'SC0-'+year+'.csv', year)
        formatear_datos(dataframe=dataframe, path=CARPETA_DATOS_FORMATEADOS+'SC0-'+year+'.csv')