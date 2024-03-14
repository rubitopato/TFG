#Librerias Necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras import backend as K

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
#from sklearn.preprocessing import scale

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

def get_equipos(dataframe: pd.DataFrame) -> list:
    list = []
    for idx in dataframe.index:
        if dataframe['HomeTeam'][idx] not in list:
            list.append(dataframe['HomeTeam'][idx])
        if dataframe['AwayTeam'][idx] not in list:
            list.append(dataframe['AwayTeam'][idx])
    return list

#Definición del Modelo
def get_modelo_regresion(features: pd.DataFrame) -> Sequential:
    numero_columnas = features.shape[1] # Numero de predictores
    print('El numero de predictores es:',numero_columnas)
    #Crear el modelo
    model = Sequential()
    model.add(Dense(10, activation='relu', input_shape=(numero_columnas,)))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(3, activation='softmax'))
    
    #Compilar modelo
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

#Plotear los datos de entrenamiento
def plot_entrenamiento(historial):
    hist = pd.DataFrame(historial.history)
    hist['epoch'] = historial.epoch

    plt.figure()
    plt.xlabel('Iteracion')
    plt.ylabel('Error')
    plt.plot(hist['epoch'], hist['loss'],label='Error Entrenamiento')
    plt.plot(hist['epoch'], hist['val_loss'],label = 'Error Valor')
    plt.legend()
    
    plt.figure()
    plt.xlabel('Iteracion')
    plt.ylabel('Precision')
    plt.plot(hist['epoch'], hist['accuracy'],label='Error Entrenamiento')
    plt.plot(hist['epoch'], hist['val_accuracy'],label = 'Error Valor')
    plt.legend()
    
    plt.show()

#Convierte numero [0,1,2] en [Away, Draw, Home]
def get_ganador_real(ganador: int) -> str:
    if (ganador==0):
      winner='Away'
    elif (ganador==1):
      winner='Draw'
    else:
      winner='Home'
    return winner

# Transforma numero en carácter
# Recibe un número [0,1,2] y dice si es [Away, Draw, Home] 
def get_ganador_prediccion(ganador: list) -> str:
  y=ganador.index(max(ganador))
  if y==0:
    pred_winner='Away'
  elif y==1:
    pred_winner='Draw'
  elif y==2:
    pred_winner='Home'
  return pred_winner

# model.predict puede dar un número muy pequeño, que debemos convertir
# en un numero "manejable"
def convertir_numbero(prediccion) -> list:
  prediccion_=[]
  for i in range(len(prediccion[0])):
    pred_number=float(format(prediccion[0][i], '.3f'))
    prediccion_.append(pred_number)

  return (prediccion_)



datos_partidos=pd.read_csv('Segundo_Dataset\Datos_Formateados\datos-1516.csv') 
print(datos_partidos.shape)
print(datos_partidos.head())

equipos = get_equipos(dataframe=datos_partidos)
print('-----------------------EQUIPOS-------------------------')
print(equipos)
print('-----------------------EQUIPOS-------------------------')

#Primero prediciremos que equipo gana sin tener en cuenta los goles porque sino xd

lb_make = LabelEncoder()
datos_partidos['target FTR'] = lb_make.fit_transform(datos_partidos['FTR'])

print('-----------------------DATOS TARGET-------------------------')
print(datos_partidos['FTR'].value_counts())
print(datos_partidos['target FTR'].value_counts())
print('-----------------------DATOS TARGET-------------------------')

#Definicion de las features (columnas utilizadas para predecir) y el target de la prediccion

columns_name=['FTHG','FTAG','HTHG','HTAG']
features = datos_partidos[columns_name]
target = datos_partidos['target FTR']

#Separacion del target en clases

target = to_categorical(target)

#Normalizacion de los datos

#print(features.head())
for col in features:
    sns.kdeplot(features[col], fill=True)
    
#METODO 1: ESTANDARIZAR
#Escalar las columnas de datos (features)

scale = StandardScaler().fit(features)
    
#Transformas las columnas de datos para que tengan una escala similar

scaled_df= scale.transform(features)
features_norm_standard= pd.DataFrame(scaled_df, columns=columns_name)

print('-----------------------FEATURES ESTANDARIZADAS-------------------------')
print(features_norm_standard.head())
print('-----------------------FEATURES ESTANDARIZADAS-------------------------')

#METODO 2: NORMALIZAR
#Escalar las columnas de datos (features)

scale_2 = MinMaxScaler().fit(features)

# transform training data
scale_df_normalize = scale_2.transform(features)
features_norm_norma= pd.DataFrame(scale_df_normalize, columns=columns_name)
print('-----------------------FEATURES NORMALIZADAS-------------------------')
features_norm_norma.head()
print('-----------------------FEATURES NORMALIZADAS-------------------------')

#Estandarizado
for col in features_norm_standard:
    sns.kdeplot(features_norm_standard[col], fill=True)
    
#Normalizado
for col in features_norm_norma:
    sns.kdeplot(features_norm_norma[col], fill=True)
    
#El metodo de normalizar consigue valores mas en el rango de [0-1] en el eje x. Este es mejor método

#Barajar y dividir las features y targets en entrenamiento y prueba
features_train, features_test, target_train, target_test = train_test_split( features_norm_norma, target, test_size=0.3, random_state=4)
print('-----------------------SETS DE ENTRENAMIENTO Y TESTEADO-------------------------')
print ('Train set:', features_train.shape,  target_train.shape)
print ('Test set:', features_test.shape,  target_test.shape)
print('-----------------------SETS DE ENTRENAMIENTO Y TESTEADO-------------------------')

#Construir el modelo

modelo = get_modelo_regresion(features=features)

#Entrenamiento del modelo

epochs=100 #iteraciones del dataset
modelo_entrenado=modelo.fit(features_train, target_train, validation_data=(features_test,target_test), epochs=epochs, verbose=2)

#Evaluacion del modelo

#Evolucion del modelo con el entrenamiento
modelo_historial = pd.DataFrame(modelo_entrenado.history)
modelo_historial['epoch'] = modelo_entrenado.epoch
#print(modelo_historial.tail())

plot_entrenamiento(modelo_entrenado)

#Evaluacion del modelo
test1 = modelo.evaluate(features_test, target_test, verbose=0)

#El error en el test:
print('-----------------------DATOS POSTENTRENAMIENTO-------------------------')
print('Test loss:', round(test1[0],3)) 
print('Test accuracy:', round(test1[1],3))
print('-----------------------DATOS POSTENTRENAMIENTO-------------------------')


#PREDICCION DE UN PARTIDO
HT='Villarreal'
AT='Levante'
datos_partido_a_predecir=datos_partidos.loc[(datos_partidos['HomeTeam']==HT) & (datos_partidos['AwayTeam']==AT)]
print(datos_partido_a_predecir.shape)
print('-----------------------DATOS PARTIDO A PREDECIR-------------------------')
print('Datos partido a predecir:',datos_partido_a_predecir)
print('-----------------------DATOS PARTIDO A PREDECIR-------------------------')

#Separar las features de la columna target
#FTR = Full Time Result (H=Home Win, D=Draw, A=Away Win)
features_2 = datos_partido_a_predecir[['FTHG','FTAG','HTHG','HTAG']]
target_2 = datos_partido_a_predecir['target FTR']
print('Features 2:',features_2)

resultado_actual=get_ganador_real(target_2)

#Normalizamos predictores
features_2_norm = (features_2 - features.mean()) / features.std()

#Predecimos el target
pred1= modelo.predict(features_2_norm)
pred1_number=convertir_numbero(pred1)
pred_winner1=get_ganador_prediccion(pred1_number)
print(pred_winner1)

print('-----------------------RESULTADOS-------------------------')
print('El ganador real es: ', resultado_actual)
print('El ganador predicho es: ',pred_winner1)
print('-----------------------RESULTADOS-------------------------')

#Ver las probabilidades del ganador en un grafico
#PIE chart
pieLabels = 'Away', 'Draw', 'Home'
figureObject, axesObject = plt.subplots()
#Draw the pie chart
axesObject.pie(pred1_number, labels=pieLabels, autopct='%1.2f', startangle=90)
# Aspect ratio - equal means pie is a circle
axesObject.axis('equal')
plt.show()