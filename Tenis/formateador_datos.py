import pandas as pd
import wget
import os
import numpy as np

random_number = np.random.randint(2)

def leer_csv(path: str, year: int) -> pd.DataFrame:
    if os.path.exists(path):
        os.remove(path)
    url='http://www.tennis-data.co.uk/'+year+'/ausopen.csv' #un final de nombre segun el campeonato
    wget.download(url, path)
    print('Datos Descargados!')
    
    dataframe_datos_partidos = pd.read_csv(path)
    return dataframe_datos_partidos

def formatear_datos(dataframe: pd.DataFrame, path: str):
    columnas = ['Tournament','Date','Series','Court','Surface','Round','Winner','Loser','WRank','LRank','WPts','LPts',
                'W1','W2','W3','W4','W5','Wsets','L1','L2','L3','L4','L5','Lsets']
    dataframe_datos_formateados = dataframe[columnas]
    for idx, partido in dataframe_datos_formateados.iterrows():
        random_number = np.random.randint(2)
        if random_number == 1:
            dataframe_datos_formateados.at[idx, 'P'] = partido['Winner']
            dataframe_datos_formateados.at[idx, 'PRank'] = partido['WRank']
            dataframe_datos_formateados.at[idx, 'PPts'] = partido['WPts']
            dataframe_datos_formateados.at[idx, 'P1'] = partido['W1']
            dataframe_datos_formateados.at[idx, 'P2'] = partido['W2']
            dataframe_datos_formateados.at[idx, 'P3'] = partido['W3']
            dataframe_datos_formateados.at[idx, 'P4'] = partido['W4']
            dataframe_datos_formateados.at[idx, 'P5'] = partido['W5']
            dataframe_datos_formateados.at[idx, 'Psets'] = partido['Wsets']
        
            dataframe_datos_formateados.at[idx, 'S'] = partido['Loser']
            dataframe_datos_formateados.at[idx, 'SRank'] = partido['LRank']
            dataframe_datos_formateados.at[idx, 'SPts'] = partido['LPts']
            dataframe_datos_formateados.at[idx, 'S1'] = partido['L1']
            dataframe_datos_formateados.at[idx, 'S2'] = partido['L2']
            dataframe_datos_formateados.at[idx, 'S3'] = partido['L3']
            dataframe_datos_formateados.at[idx, 'S4'] = partido['L4']
            dataframe_datos_formateados.at[idx, 'S5'] = partido['L5']
            dataframe_datos_formateados.at[idx, 'Ssets'] = partido['Lsets']
            
            dataframe_datos_formateados.at[idx, 'Gana_P'] = 1
        
        else:
            dataframe_datos_formateados.at[idx, 'P'] = partido['Loser']
            dataframe_datos_formateados.at[idx, 'PRank'] = partido['LRank']
            dataframe_datos_formateados.at[idx, 'PPts'] = partido['LPts']
            dataframe_datos_formateados.at[idx, 'P1'] = partido['L1']
            dataframe_datos_formateados.at[idx, 'P2'] = partido['L2']
            dataframe_datos_formateados.at[idx, 'P3'] = partido['L3']
            dataframe_datos_formateados.at[idx, 'P4'] = partido['L4']
            dataframe_datos_formateados.at[idx, 'P5'] = partido['L5']
            dataframe_datos_formateados.at[idx, 'Psets'] = partido['Lsets']
        
            dataframe_datos_formateados.at[idx, 'S'] = partido['Winner']
            dataframe_datos_formateados.at[idx, 'SRank'] = partido['WRank']
            dataframe_datos_formateados.at[idx, 'SPts'] = partido['WPts']
            dataframe_datos_formateados.at[idx, 'S1'] = partido['W1']
            dataframe_datos_formateados.at[idx, 'S2'] = partido['W2']
            dataframe_datos_formateados.at[idx, 'S3'] = partido['W3']
            dataframe_datos_formateados.at[idx, 'S4'] = partido['W4']
            dataframe_datos_formateados.at[idx, 'S5'] = partido['W5']
            dataframe_datos_formateados.at[idx, 'Ssets'] = partido['Wsets']
            
            dataframe_datos_formateados.at[idx, 'Gana_P'] = 0 

    columnas = ['Tournament','Date','Series','Court','Surface','Round','P','S','PRank','SRank','PPts','SPts',
                'P1','S1','P2','S2','P3','S3','P4','S4','P5','S5','Psets','Ssets','Gana_P']
    
    dataframe_final = dataframe_datos_formateados[columnas]
    
    if os.path.exists(path):
        os.remove(path)
    dataframe_final.to_csv(path, index=False)
    
if __name__ == "__main__":
    years = ['2006','2007','2008','2009','2010','2011','2012','2013',
             '2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']
    CARPETA_DATOS_PUROS = "C:/Users/User/OneDrive/Escritorio/Cosas_TFG/Tenis/Datos_Puros/"
    CARPETA_DATOS_FORMATEADOS = "C:/Users/User/OneDrive/Escritorio/Cosas_TFG/Tenis/Datos_Formateados/"
    for year in years:
        dataframe = leer_csv(CARPETA_DATOS_PUROS+year+'-ausopen.csv', year) #para cada campeonato se especifica un final segun la pagina
        formatear_datos(dataframe=dataframe, path=CARPETA_DATOS_FORMATEADOS+year+'-ausopen.csv')