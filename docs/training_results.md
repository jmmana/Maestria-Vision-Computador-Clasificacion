# Argos — Resultados del entrenamiento

> 📝 Este documento se completa después del entrenamiento en AWS Rekognition Custom Labels.

---

## Configuración del entrenamiento

| Parámetro | Valor |
|-----------|-------|
| Plataforma | AWS Rekognition Custom Labels |
| Tipo de proyecto | Classification |
| Tipo de clasificación | Multiclass (Single tag per image) |
| Modo de entrenamiento | Quick Training |
| Split | 80% entrenamiento / 20% prueba |
| Fecha de entrenamiento | 2026-05-24 |
| Región | us-east-1 |

---

## Dataset

| Clase | Imágenes totales | Train | Test |
|-------|-----------------|-------|------|
| Elephant | 17 | ~14 | ~3 |
| Giraffe | 17 | ~14 | ~3 |
| Lion | 17 | ~14 | ~3 |
| **Total** | **51** | **~41** | **~9** |

---

## Métricas de rendimiento

> *(Completar con los valores reales de la consola AWS)*

| Clase | Precision | Recall |
|-------|-----------|--------|
| Elephant | ___% | ___% |
| Giraffe | ___% | ___% |
| Lion | ___% | ___% |
| **Promedio** | **___%** | **___%** |

### Interpretación

- **Precision:** De todas las veces que el modelo predijo "elephant", ¿cuántas veces tenía razón?
- **Recall:** De todas las imágenes reales de "elephant", ¿cuántas detectó el modelo?

---

## Pruebas manuales (Quick Test)

| Imagen | Predicción | Confianza | Correcto |
|--------|-----------|-----------|---------|
| test_1.jpg | — | —% | — |
| test_2.jpg | — | —% | — |
| test_3.jpg | — | —% | — |
| test_4.jpg | — | —% | — |
| test_5.jpg | — | —% | — |

---

## Observaciones

*(Añadir observaciones sobre el rendimiento del modelo, clases con mayor dificultad, etc.)*

---

## Endpoint del modelo publicado

```
Project ARN  : arn:aws:rekognition:us-east-1:XXXXXXXXXXXX:project/Argos/...
Model ARN    : arn:aws:rekognition:us-east-1:XXXXXXXXXXXX:project/Argos/version/.../...
Prediction URL: (disponible vía SDK Boto3)
```
