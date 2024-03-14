import pandas as pd

def leer_partidos_csv(path: str) -> pd.DataFrame:
    datos_partidos_dataframe = pd.read_csv(path)
    datos_partidos_dataframe = datos_partidos_dataframe.astype({'league': 'str'}) #convertir columna league en string
    #quitar espacios, : y poner todo en minusculas
    datos_partidos_dataframe['league_formateada'] = datos_partidos_dataframe['league'].apply(lambda liga: liga.strip().replace(":","").lower().replace(" ","")) 
    league = "spainprimeradivision"
    datos_partidos_spain_dataframe = datos_partidos_dataframe.query('league_formateada == @league') # Solo quiero las filas de la liga española
    datos_partidos_spain_dataframe['match_date_formateada'] = datos_partidos_spain_dataframe['match_date'].apply(lambda date: date.replace("-",""))
    datos_partidos_spain_dataframe = datos_partidos_spain_dataframe.astype({'match_date_formateada': 'int'})
    datos_partidos_spain_date_dataframe = datos_partidos_spain_dataframe.query('match_date_formateada <= 20080201')
    return datos_partidos_spain_date_dataframe

def escribir_partidos_csv(dataframe: pd.DataFrame, path: str):
    columnas = ['league','match_date','home_team','home_score','away_team','away_score']
    dataframe_columnas_seleccionadas = dataframe[columnas]
    dataframe_columnas_seleccionadas.to_csv(path, index=False)
    
if __name__ == "__main__":
    dataframe = leer_partidos_csv("Datasets/Partidos/closing_odds.csv")
    escribir_partidos_csv(dataframe=dataframe, path="Datos_Formateados/datos_partidos.csv")

