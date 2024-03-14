import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras import layers, models

tfd = tfp.distributions
tfpl = tfp.layers

# Supongamos que tienes datos de entrada X y objetivos de regresión y

# Construir el modelo
model = models.Sequential([
    layers.Input(shape=(input_shape,)),
    tfpl.DenseFlipout(64, activation='relu'),  # Capa bayesiana con dropout específico para redes bayesianas
    tfpl.DenseFlipout(32, activation='relu'),
    tfpl.DenseFlipout(1)  # Capa de salida para la regresión bayesiana
])

# Compilar el modelo con una función de pérdida adecuada para regresión bayesiana
model.compile(optimizer='adam', loss=lambda y_true, y_pred: -y_pred.log_prob(y_true))

# Entrenar el modelo con tus datos
model.fit(X, y, epochs=10, batch_size=32)

# Hacer predicciones
predictions = model.predict(X)

# Acceder a la distribución de probabilidad de las predicciones
predicted_distribution = model(X)
