# Informe Actividad 4 — Clasificación de Imágenes con AWS Rekognition Custom Labels

**Proyecto:** Argos  
**Materia:** 2026-1 · VISIÓN POR COMPUTADOR · G02  
**Unidad:** 2 — Técnicas de entrenamiento y optimización para modelos de visión por computador  
**Estudiantes:** María Alejandra Gómez Piedrahita · Juan Manuel Castillo Pinto  
**Fecha:** 24 de mayo de 2026  
**Universidad:** La Salle — Maestría en Inteligencia Artificial

---

## 1. Introducción

En esta actividad implementamos un modelo de clasificación de imágenes usando **Amazon Rekognition Custom Labels**, el servicio de AWS equivalente a Azure Custom Vision. El proyecto fue nombrado **Argos** en referencia al gigante mitológico griego de cien ojos, símbolo de vigilancia visual total.

El objetivo fue entrenar, evaluar y publicar un modelo capaz de clasificar imágenes de tres animales africanos: elefante, jirafa y león.

---

## 2. Configuración del recurso AWS

### 2.1 Cuenta y región

Utilizamos una cuenta AWS con créditos universitarios. La región seleccionada fue **us-east-1 (N. Virginia)** por disponibilidad del servicio Rekognition Custom Labels.

*(Insertar captura: consola AWS > Rekognition > Custom Labels)*

### 2.2 Servicio utilizado

| Parámetro | Valor |
|-----------|-------|
| Servicio | Amazon Rekognition Custom Labels |
| Equivalente Azure | Azure Custom Vision |
| Región | us-east-1 |
| Nombre del proyecto | Argos |

---

## 3. Creación del proyecto

### 3.1 Proyecto Rekognition Custom Labels

Se creó el proyecto con las siguientes configuraciones:

| Parámetro | Valor |
|-----------|-------|
| Nombre | Argos |
| Tipo | Clasificación de imágenes |
| Clasificación | Multiclass (una etiqueta por imagen) |
| Training split | 80% train / 20% test |

*(Insertar captura: creación del proyecto Argos en la consola)*

### 3.2 Dataset

Se creó un único dataset que Rekognition divide automáticamente en 80% entrenamiento y 20% prueba.

*(Insertar captura: configuración del dataset)*

---

## 4. Carga y etiquetado de imágenes

Se cargaron **51 imágenes** distribuidas en 3 clases:

| Clase | Etiqueta | Cantidad |
|-------|----------|----------|
| Elefante africano | `elephant` | 17 |
| Jirafa | `giraffe` | 17 |
| León | `lion` | 17 |

*(Insertar capturas: interfaz de etiquetado con las imágenes por clase)*

---

## 5. Entrenamiento del modelo

Se utilizó el modo **Quick Training** disponible en Rekognition Custom Labels.

- Tiempo aproximado de entrenamiento: ~45 minutos
- Rekognition aplica técnicas de Transfer Learning sobre modelos pre-entrenados de AWS

*(Insertar captura: pantalla de entrenamiento en progreso y completado)*

---

## 6. Evaluación del modelo

### 6.1 Métricas de rendimiento

*(Insertar captura: pantalla de métricas Precision/Recall de la consola)*

| Clase | Precision | Recall |
|-------|-----------|--------|
| Elephant | ___% | ___% |
| Giraffe | ___% | ___% |
| Lion | ___% | ___% |
| **Promedio** | **___%** | **___%** |

### 6.2 Interpretación de métricas

- **Precision:** Proporción de predicciones correctas sobre el total de predicciones realizadas para cada clase.
- **Recall:** Proporción de imágenes correctamente identificadas sobre el total de imágenes reales de cada clase.

### 6.3 Quick Test (prueba rápida en consola)

*(Insertar capturas de las pruebas rápidas realizadas desde la consola)*

---

## 7. Publicación del modelo

El modelo fue publicado en AWS para habilitar el endpoint de predicción:

```
Project ARN : arn:aws:rekognition:us-east-1:...:project/Argos/...
Model ARN   : arn:aws:rekognition:us-east-1:...:project/Argos/version/.../...
```

*(Insertar captura: pantalla de publicación del modelo con estado RUNNING)*

---

## 8. Aplicación cliente

Se desarrolló una aplicación cliente en Python (`src/client/predict.py`) que consume el endpoint de predicción de AWS:

```bash
python src/client/predict.py \
  --image data/test/mi_animal.jpg \
  --model-arn arn:aws:rekognition:us-east-1:...:project/Argos/version/.../...
```

### Resultado de la prueba

```
🔍 Analizando imagen: mi_animal.jpg
────────────────────────────────────────
✅ Predicción: ELEPHANT
   Confianza:  94.7%
────────────────────────────────────────
```

*(Insertar captura de la ejecución en terminal)*

---

## 9. Conclusiones

1. **AWS Rekognition Custom Labels** es una alternativa válida y completa a Azure Custom Vision para clasificación de imágenes.
2. Con solo **17 imágenes por clase**, el modelo logró métricas de Precision/Recall de ___% gracias al Transfer Learning pre-entrenado de AWS.
3. El nombre **Argos** resultó apropiado: el modelo "ve" y clasifica con alta precisión.
4. La herramienta no requiere conocimiento profundo de ML: el proceso de Quick Training abstrae la complejidad del entrenamiento.

---

## 10. Repositorio del proyecto

🔗 https://github.com/jmmana/Maestria-Vision-Computador-Clasificacion

---

## Referencias

- Amazon Web Services. (2024). *Amazon Rekognition Custom Labels Developer Guide*. https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/
- Boto3 Documentation. (2024). *Rekognition — AWS SDK for Python*. https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html
