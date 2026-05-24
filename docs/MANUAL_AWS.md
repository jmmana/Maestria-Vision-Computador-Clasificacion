# Manual del proceso — Argos en AWS Rekognition Custom Labels

**Proyecto:** Argos  
**Plataforma:** Amazon Rekognition Custom Labels — us-east-1  
**Project ARN:** `arn:aws:rekognition:us-east-1:442444704156:project/Argos/1779659669813`  
**Autores:** María Alejandra Gómez Piedrahita · Juan Manuel Castillo Pinto  
**Materia:** 2026-1 · VISIÓN POR COMPUTADOR · G02

---

## Paso 1 — Acceso a Rekognition Custom Labels

Ingresar a: https://us-east-1.console.aws.amazon.com/rekognition/custom-labels

El proyecto **Argos** fue creado en la región **us-east-1 (N. Virginia)**.

---

## Paso 2 — Crear conjunto de datos

Se configuró el dataset con las siguientes opciones:
- ✅ **"Comience con un único conjunto de datos"** — división automática 80% entrenamiento / 20% prueba
- ✅ **"Cargar imágenes desde el equipo"**

![Crear conjunto de datos](screenshots/Crear%20Conjunto%20de%20datos.png)

---

## Paso 3 — Agregar imágenes al conjunto de datos

Las imágenes fueron subidas en 3 tandas (una por clase) para facilitar el etiquetado:

| Clase | Imágenes | Etiqueta |
|-------|----------|----------|
| 🐘 Elefante | 17 | `elephant` |
| 🦒 Jirafa | 17 | `giraffe` |
| 🦁 León | 17 | `lion` |

![Agregar imágenes](screenshots/Agregar%20imagenes%20al%20conjunto%20de%20datos.png)

---

## Paso 4 — Crear etiquetas (labels)

Se crearon 3 etiquetas de clasificación: `elephant`, `giraffe`, `lion`.

![Crear etiquetas](screenshots/Crear%20Etiquetas%20para%20el%20conjunto%20de%20datos.png)

---

## Paso 5 — Dataset completo con imágenes etiquetadas

Las 51 imágenes fueron etiquetadas correctamente: **17 por cada categoría**.

![Imágenes etiquetadas](screenshots/Imagenes%20Etiquedatas%2017%20por%20categorias.png)

### Detalle del conjunto de datos

![Detalle dataset](screenshots/Detalle%20del%20conjunto%20de%20datos.png)

---

## Paso 6 — Entrenar el modelo

Se inició el entrenamiento desde la pantalla **"Modelo de entrenamiento"**.

El proyecto fue seleccionado automáticamente con su ARN:
```
arn:aws:rekognition:us-east-1:442444704156:project/Argos/1779659669813
```

![Modelo de entrenamiento](screenshots/Modelo%20de%20entrenamiento.png)

> ⏳ El entrenamiento tarda aproximadamente **45 minutos**.  
> AWS usa Transfer Learning sobre modelos pre-entrenados para clasificación multiclase.

---

## Paso 7 — Evaluar el modelo

*(Capturas pendientes — completar después del entrenamiento)*

Una vez completado, la consola mostrará las métricas de **Precision** y **Recall** por clase.

| Clase | Precision | Recall |
|-------|-----------|--------|
| Elephant | ___% | ___% |
| Giraffe | ___% | ___% |
| Lion | ___% | ___% |

---

## Paso 8 — Quick Test (pruebas rápidas)

*(Capturas pendientes)*

---

## Paso 9 — Publicar modelo

*(Capturas pendientes)*

```
Model ARN: arn:aws:rekognition:us-east-1:442444704156:project/Argos/version/...
```

---

## Paso 10 — App cliente (predict.py)

```bash
pip install boto3

python src/client/predict.py \
  --image data/test/mi_animal.jpg \
  --model-arn arn:aws:rekognition:us-east-1:442444704156:project/Argos/version/...
```

---

## Resumen de infraestructura AWS

| Recurso | Valor |
|---------|-------|
| Servicio | Amazon Rekognition Custom Labels |
| Región | us-east-1 (N. Virginia) |
| Proyecto | Argos |
| Project ARN | `arn:aws:rekognition:us-east-1:442444704156:project/Argos/1779659669813` |
| Dataset | 51 imágenes · 3 clases · 17 imgs/clase |
| Entrenamiento | Quick Training |
