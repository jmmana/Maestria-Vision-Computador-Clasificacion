# Manual del proceso — Argos en AWS Rekognition Custom Labels

**Proyecto:** Argos  
**Plataforma:** Amazon Rekognition Custom Labels — us-east-1  
**Autores:** María Alejandra Gómez Piedrahita · Juan Manuel Castillo Pinto

---

## Paso 1 — Acceso a Rekognition Custom Labels

Ingresar a: https://us-east-1.console.aws.amazon.com/rekognition/custom-labels

![Página principal Custom Labels](screenshots/01_rekognition_custom_labels_home.png)

---

## Paso 2 — Proyecto Argos

El proyecto fue creado con el nombre **Argos**.

![Proyecto Argos](screenshots/02_proyecto_argos_creado.png)

---

## Paso 3 — Crear dataset

Configuración seleccionada:
- ✅ **Comience con un único conjunto de datos** (80% train / 20% test automático)
- ✅ **Cargar imágenes desde el equipo**

![Crear dataset](screenshots/03_crear_dataset_config.png)

---

## Paso 4 — Subir imágenes de entrenamiento

Se subieron **51 imágenes** en 3 grupos:

### 🐘 Elefantes (17 imágenes)
![Subida elephant](screenshots/04_subir_imagenes_elephant.png)

### 🦒 Jirafas (17 imágenes)
![Subida giraffe](screenshots/05_subir_imagenes_giraffe.png)

### 🦁 Leones (17 imágenes)
![Subida lion](screenshots/06_subir_imagenes_lion.png)

---

## Paso 5 — Etiquetar imágenes

Cada conjunto de imágenes fue etiquetado con su respectiva clase.

### Etiqueta: `elephant`
![Etiquetado elephant](screenshots/07_etiquetado_elephant.png)

### Etiqueta: `giraffe`
![Etiquetado giraffe](screenshots/08_etiquetado_giraffe.png)

### Etiqueta: `lion`
![Etiquetado lion](screenshots/09_etiquetado_lion.png)

### Dataset completo (51 imágenes etiquetadas)
![Dataset completo](screenshots/10_dataset_completo_51_imagenes.png)

---

## Paso 6 — Entrenar el modelo

Se seleccionó **Quick Training** y se inició el entrenamiento.

![Iniciar entrenamiento](screenshots/11_iniciar_entrenamiento.png)

### Entrenamiento en progreso (~45 minutos)
![En progreso](screenshots/12_entrenamiento_en_progreso.png)

### Entrenamiento completado
![Completado](screenshots/13_entrenamiento_completado.png)

---

## Paso 7 — Evaluar el modelo

### Métricas de Precision y Recall

![Métricas](screenshots/14_metricas_precision_recall.png)

| Clase | Precision | Recall |
|-------|-----------|--------|
| Elephant | ___% | ___% |
| Giraffe | ___% | ___% |
| Lion | ___% | ___% |

### Quick Test — Pruebas rápidas

![Test elephant](screenshots/15_quick_test_elephant.png)
![Test giraffe](screenshots/16_quick_test_giraffe.png)
![Test lion](screenshots/17_quick_test_lion.png)

---

## Paso 8 — Publicar el modelo

Se publicó el modelo para habilitar el endpoint de predicción.

![Publicar modelo](screenshots/18_publicar_modelo.png)
![Modelo RUNNING](screenshots/19_modelo_running.png)

```
Model ARN: arn:aws:rekognition:us-east-1:XXXXXXXXXXXX:project/Argos/version/.../...
```

---

## Paso 9 — App cliente (predict.py)

```bash
pip install boto3
python src/client/predict.py \
  --image data/test/mi_animal.jpg \
  --model-arn arn:aws:rekognition:us-east-1:...:project/Argos/version/.../...
```

![Terminal predict.py](screenshots/20_predict_py_terminal.png)

---

## Resumen de recursos AWS utilizados

| Recurso | Nombre | Región | Costo estimado |
|---------|--------|--------|---------------|
| Rekognition Custom Labels | Argos | us-east-1 | ~$1 USD (training) |
| Endpoint de predicción | Argos v1 | us-east-1 | $0.01/imagen |
