import pandas as pd
import wget
import os

def formatear_datos(dataframe: pd.DataFrame):
    columnas = ['game_id','season','type','date_time_GMT','home_team_id','away_team_id','home_goals','away_goals','outcome']
    dataframe_datos_puros = dataframe[columnas]
    for idx, partido in dataframe_datos_puros.iterrows():
        if partido['outcome'] == 'home win REG' or partido['outcome'] == 'home win OT':
            dataframe_datos_puros.at[idx, 'home_wins'] = 1
        if partido['outcome'] == 'away win REG' or partido['outcome'] == 'away win OT':
            dataframe_datos_puros.at[idx, 'home_wins'] = 0
        if partido['outcome'] == 'away win OT' or partido['outcome'] == 'home win OT':
            dataframe_datos_puros.at[idx, 'overtime'] = 1
        if partido['outcome'] == 'away win REG' or partido['outcome'] == 'home win REG':
            dataframe_datos_puros.at[idx, 'overtime'] = 0
    dataframe_datos_puros['season'] = dataframe_datos_puros['season'].astype(int)
    dataframe_datos_puros = dataframe_datos_puros.sort_values(by=['season', 'date_time_GMT'], ascending=True)
    dataframe_datos_puros.to_csv("C:/Users/User/OneDrive/Escritorio/Cosas_TFG/Hockey/Datos_Formateados/games.csv")
    
if __name__ == "__main__":
    dataframe = pd.read_csv("C:/Users/User/OneDrive/Escritorio/Cosas_TFG/Hockey/Datos_Puros/game.csv")
    formatear_datos(dataframe=dataframe)