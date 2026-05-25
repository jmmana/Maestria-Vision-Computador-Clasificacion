# Argos: Sistema de Clasificación de Imágenes mediante Aprendizaje Automático en la Nube

[![AWS Rekognition](https://img.shields.io/badge/AWS-Rekognition%20Custom%20Labels-FF9900?style=flat-square&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/rekognition/custom-labels-features/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Estado](https://img.shields.io/badge/Estado-Completado-2ea44f?style=flat-square)](https://github.com/jmmana/Maestria-Vision-Computador-Clasificacion)

---

**Materia:** 2026-1 · Visión por Computador · Grupo 02  
**Unidad:** 2 — Técnicas de entrenamiento y optimización para modelos de visión por computador  
**Actividad:** 4 — Implementación de un modelo de clasificación de imágenes  
**Institución:** Universidad de La Salle · Maestría en Inteligencia Artificial · Bogotá, Colombia  
**Fecha:** Mayo 24 de 2026

| Rol | Nombre |
|-----|--------|
| Investigadora principal | María Alejandra Gómez Piedrahita |
| Arquitecto de solución | Juan Manuel Castillo Pinto |

---

## Resumen

Este trabajo presenta el diseño, implementación y evaluación de **Argos**, un sistema de clasificación automática de imágenes de fauna africana desarrollado como parte de la Actividad 4 de la asignatura Visión por Computador. El sistema emplea el servicio **Amazon Rekognition Custom Labels** como plataforma de Machine Learning en la nube, siguiendo una metodología de **Spec Driven Design** que define formalmente los requisitos antes de la implementación. El modelo fue entrenado con un conjunto de datos de 51 imágenes distribuidas en tres clases (elefante, jirafa y león), alcanzando métricas satisfactorias de Precision y Recall mediante Quick Training con Transfer Learning. El sistema fue extendido con una aplicación web moderna desplegada en infraestructura de nube, que permite la clasificación interactiva de imágenes y la gestión del ciclo de vida del modelo.

**Palabras clave:** clasificación de imágenes, aprendizaje automático, visión por computador, AWS Rekognition, Transfer Learning, aplicación web, nube.

---

## 1. Introducción

La clasificación automática de imágenes es una de las tareas fundamentales en el campo de la visión por computador. Con el advenimiento de los servicios de inteligencia artificial en la nube, es posible construir modelos de clasificación de alta precisión sin necesidad de infraestructura propia ni conocimiento profundo de arquitecturas de redes neuronales.

El nombre **Argos** hace referencia a *Argos Panoptes*, el gigante de la mitología griega que poseía cien ojos y lo observaba todo. Esta metáfora resulta especialmente adecuada para un sistema cuyo propósito es identificar y clasificar el contenido visual de imágenes.

### 1.1 Objetivos

- Crear y configurar un proyecto de clasificación de imágenes en una plataforma de IA en la nube (AWS Rekognition Custom Labels).
- Construir y etiquetar un conjunto de datos de entrenamiento con tres clases de fauna africana.
- Entrenar y evaluar un modelo de clasificación multiclase utilizando Transfer Learning.
- Publicar el modelo como endpoint de predicción accesible mediante API.
- Desarrollar una aplicación cliente que consuma el endpoint y permita clasificar imágenes de forma interactiva.

### 1.2 Plataforma seleccionada

Se eligió **Amazon Rekognition Custom Labels** como alternativa a Azure Custom Vision, dado que el equipo contaba con créditos AWS. Rekognition Custom Labels es el equivalente funcional directo: permite entrenar modelos de clasificación multiclase con imágenes propias, sin requerir experiencia en ML, y expone un endpoint de predicción mediante AWS SDK.

---

## 2. Metodología

### 2.1 Spec Driven Design

El proyecto siguió la metodología **Spec Driven Design (SDD)**: todos los requisitos, criterios de éxito, arquitectura y entregables fueron formalizados en el documento [`SPEC.md`](SPEC.md) antes de escribir una sola línea de código o configurar cualquier recurso en la nube. Esta aproximación garantiza trazabilidad entre los requisitos académicos y la implementación técnica.

### 2.2 Arquitectura general

```
[Dataset local · 51 imágenes]
           │
           ▼
[AWS Rekognition Custom Labels]
  ├── Proyecto: Argos
  ├── Dataset: 80% entrenamiento / 20% evaluación
  ├── Entrenamiento: Quick Training (Transfer Learning)
  └── Modelo publicado ──► Endpoint ARN
           │
    ┌──────┴──────┐
    ▼             ▼
[CLI predict.py]  [Web App · argos.warlockcode.com]
```

### 2.3 Dataset

El conjunto de datos fue proporcionado por la cátedra y contiene imágenes de fauna africana en formato JPG. La distribución es la siguiente:

| Clase | Etiqueta | Cantidad | Proporción train | Proporción test |
|-------|----------|----------|-----------------|-----------------|
| Elefante africano | `elephant` | 17 | ~14 | ~3 |
| Jirafa | `giraffe` | 17 | ~14 | ~3 |
| León | `lion` | 17 | ~14 | ~3 |
| **Total** | — | **51** | **~41** | **~9** |

AWS Rekognition aplica automáticamente la división 80/20 entre entrenamiento y prueba.

---

## 3. Implementación en AWS

### 3.1 Configuración del proyecto

Se creó un proyecto en Amazon Rekognition Custom Labels denominado **Argos**, en la región `us-east-1` (Norte de Virginia). Los identificadores del proyecto son:

```
Project ARN : arn:aws:rekognition:us-east-1:442444704156:project/Argos/1779659669813
Model ARN   : arn:aws:rekognition:us-east-1:442444704156:project/Argos/version/Argos.2026-05-24T18.36.39/1779665799778
Región      : us-east-1 (N. Virginia)
```

### 3.2 Creación del conjunto de datos

Se configuró un único dataset con división automática 80/20. Las imágenes fueron cargadas desde el equipo local en tres tandas (una por clase) para facilitar el proceso de etiquetado.

![Configuración del conjunto de datos](docs/screenshots/Crear%20Conjunto%20de%20datos.png)
*Figura 1. Configuración del conjunto de datos con división 80% entrenamiento / 20% evaluación.*

![División 80/20 del dataset](docs/screenshots/Modeo%20de%20formacion%2080%20.png)
*Figura 2. Parámetros de configuración: conjunto único con partición automática.*

### 3.3 Carga y etiquetado de imágenes

Las 51 imágenes fueron cargadas y etiquetadas mediante la interfaz de Rekognition Custom Labels, asignando a cada imagen su clase correspondiente (`elephant`, `giraffe` o `lion`).

![Interfaz de carga de imágenes](docs/screenshots/Agregar%20imagenes%20al%20conjunto%20de%20datos.png)
*Figura 3. Interfaz de carga de imágenes al conjunto de datos.*

![Creación de etiquetas de clasificación](docs/screenshots/Crear%20Etiquetas%20para%20el%20conjunto%20de%20datos.png)
*Figura 4. Creación de las etiquetas de clasificación: elephant, giraffe, lion.*

![Imágenes etiquetadas por categoría](docs/screenshots/Imagenes%20Etiquedatas%2017%20por%20categorias.png)
*Figura 5. Distribución del dataset: 17 imágenes etiquetadas por cada categoría.*

![Detalle del conjunto de datos](docs/screenshots/Detalle%20del%20conjunto%20de%20datos.png)
*Figura 6. Vista de detalle del conjunto de datos con las imágenes organizadas.*

### 3.4 Entrenamiento del modelo

Se utilizó la modalidad **Quick Training**, que aplica Transfer Learning sobre modelos pre-entrenados de AWS para acelerar el proceso de entrenamiento. Esta modalidad es adecuada para conjuntos de datos pequeños (< 500 imágenes por clase).

![Configuración del entrenamiento](docs/screenshots/Modelo%20de%20entrenamiento.png)
*Figura 7. Pantalla de configuración del modelo de entrenamiento con el ARN del proyecto.*

![Entrenamiento en progreso](docs/screenshots/Modelo%20en%20entrenamiento.png)
*Figura 8. Proceso de entrenamiento en curso. Duración aproximada: 45 minutos.*

![Entrenamiento completado](docs/screenshots/Modelo%20Entrenado.png)
*Figura 9. Entrenamiento completado exitosamente. El modelo queda listo para evaluación.*

---

## 4. Evaluación del modelo

### 4.1 Métricas de rendimiento

Una vez completado el entrenamiento, Rekognition Custom Labels proporciona automáticamente las métricas de **Precision** y **Recall** para cada clase, calculadas sobre el conjunto de evaluación (20% del dataset).

![Métricas de evaluación del modelo](docs/screenshots/Evaluacion%20del%20modelo.png)
*Figura 10. Métricas de Precision y Recall por clase del modelo entrenado.*

![Detalles del modelo entrenado](docs/screenshots/Detalle%20del%20modelo.png)
*Figura 11. Vista de detalles del modelo con configuración y métricas globales.*

![Proyecto completado en AWS](docs/screenshots/Projecto%20de%20AWS%20entrenado.png)
*Figura 12. Vista general del proyecto Argos en AWS Rekognition Custom Labels.*

### 4.2 Interpretación de las métricas

| Métrica | Definición |
|---------|-----------|
| **Precision** | De todas las imágenes que el modelo clasificó como clase X, ¿qué fracción era realmente de clase X? Mide la tasa de falsos positivos. |
| **Recall** | De todas las imágenes reales de clase X, ¿qué fracción fue correctamente identificada por el modelo? Mide la tasa de falsos negativos. |

Un valor alto en ambas métricas indica un modelo robusto. La limitación principal del dataset es su tamaño reducido (17 imágenes/clase), mitigado por el uso de Transfer Learning.

---

## 5. Publicación y uso del modelo

### 5.1 Publicación del endpoint

El modelo fue publicado en AWS como endpoint de predicción activo. Para iniciarlo:

```bash
aws rekognition start-project-version \
  --project-version-arn "arn:aws:rekognition:us-east-1:442444704156:project/Argos/version/Argos.2026-05-24T18.36.39/1779665799778" \
  --min-inference-units 1 \
  --region us-east-1
```

### 5.2 Aplicación cliente CLI

Se desarrolló una aplicación cliente en Python (`src/client/predict.py`) que consume directamente el endpoint de AWS sin necesidad de S3:

```bash
# Instalación
pip install boto3

# Clasificar una imagen
python src/client/predict.py --image foto_animal.jpg

# Gestión del modelo
python src/client/predict.py --start-model   # Inicia el endpoint
python src/client/predict.py --stop-model    # Detiene el endpoint
```

**Salida de ejemplo:**

```
Analizando imagen: foto_animal.jpg
----------------------------------------
Prediccion : ELEPHANT
Confianza  : 94.7%
----------------------------------------
```

### 5.3 Aplicación web interactiva

Como extensión de la entrega, se desarrolló una aplicación web moderna accesible en:

**[argos.warlockcode.com](https://argos.warlockcode.com)**

La aplicación incluye:

| Funcionalidad | Descripción |
|--------------|-------------|
| Autenticación | Login con usuario y contraseña |
| Estado del modelo | Indicador en tiempo real (activo / inactivo) |
| Control del modelo | Botones para encender y detener el endpoint AWS |
| Auto-apagado | Cierre automático tras 60 minutos para control de costos |
| Clasificación | Carga de imagen por drag-and-drop con efecto visual de procesamiento |
| Resultados | Clase predicha con porcentaje de confianza y barras animadas |
| Log de actividad | Registro en tiempo real de cada operación con timestamp UTC |

**Stack tecnológico de la aplicación web:**

```
Backend  : Python · FastAPI · boto3 · APScheduler
Frontend : TailwindCSS · Alpine.js
Deploy   : Docker · Coolify · argos.warlockcode.com
```

#### Pantallas de la aplicación

**Figura 1 — Landing page y autenticación**

![Login de Argos](docs/screenshots/Argos%20login.png)

*Página de inicio con presentación del proyecto y formulario de autenticación. Acceso: usuario `admin`, contraseña `argos2026lasalle`.*

---

**Figura 2 — Dashboard con modelo activo**

![Dashboard de Argos](docs/screenshots/argos%20dasboad.png)

*Dashboard principal. El banner verde confirma que el modelo AWS está en estado RUNNING y listo para clasificar. El log de actividad en la parte inferior registra cada operación con timestamp UTC.*

---

**Figura 3 — Módulo clasificador**

![Clasificador de imágenes](docs/screenshots/Clasificador%20de%20imagenes.png)

*Módulo de clasificación con área de drag-and-drop activa. El botón "Clasificar imagen" se habilita automáticamente al cargar una imagen.*

---

**Figura 4 — Imagen cargada, lista para clasificar**

![Imagen cargada](docs/screenshots/Clasificador%20de%20imagenes%20con%20imagen.png)

*Preview inmediato de la imagen seleccionada. La imagen se envía al backend como bytes (sin S3) y FastAPI la reenvía a `detect_custom_labels` de AWS Rekognition.*

---

**Figura 5 — Resultado de clasificación**

![Resultado de clasificación](docs/screenshots/Clasificador%20de%20imagen%20con%20imagen%20clasificada.png)

*Resultado de clasificación exitosa: clase predicha (ELEPHANT) con porcentaje de confianza y barra de progreso animada. El evento queda registrado en el log de actividad.*

---

## 6. Estructura del repositorio

```
Argos/
├── README.md                        # Este documento
├── SPEC.md                          # Especificación Spec Driven Design
├── .gitignore
│
├── data/
│   ├── training/
│   │   ├── elephant/                # 17 imágenes de entrenamiento
│   │   ├── giraffe/                 # 17 imágenes de entrenamiento
│   │   └── lion/                    # 17 imágenes de entrenamiento
│   └── test/                        # Imágenes para pruebas del cliente
│
├── src/
│   └── client/
│       └── predict.py               # Aplicación cliente CLI
│
├── web/                             # Aplicación web
│   ├── main.py                      # Backend FastAPI
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .env.example
│   └── templates/
│       ├── index.html               # Landing page + login
│       └── dashboard.html           # Clasificador interactivo
│
└── docs/
    ├── MANUAL_AWS.md                # Manual paso a paso del proceso AWS
    ├── training_results.md          # Métricas de entrenamiento
    └── screenshots/                 # Evidencia fotográfica del proceso
```

---

## 7. Reproducibilidad

### Prerrequisitos

```bash
# Python 3.11+
pip install boto3

# Configurar credenciales AWS
aws configure
# AWS Access Key ID     : <clave>
# AWS Secret Access Key : <secreto>
# Default region        : us-east-1
# Output format         : json
```

### Clonar y ejecutar

```bash
git clone https://github.com/jmmana/Maestria-Vision-Computador-Clasificacion.git
cd Maestria-Vision-Computador-Clasificacion

# Clasificar una imagen de prueba
python src/client/predict.py --image data/training/elephant/Picture24.jpg
```

### Desplegar la aplicación web localmente

```bash
cd web
cp .env.example .env
# Editar .env con credenciales reales

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# Abrir http://localhost:8000
```

---

## 8. Criterios de evaluación cumplidos

| Criterio | Puntos | Evidencia |
|----------|--------|-----------|
| Creación y configuración del recurso AWS AI Services | 1 / 1 | Figuras 1–2 · Project ARN |
| Creación y configuración del proyecto de clasificación | 2 / 2 | Figuras 3–6 · Dataset etiquetado |
| Entrenamiento y evaluación del modelo | 1 / 1 | Figuras 7–11 · Métricas Precision/Recall |
| Publicar y probar el modelo con aplicación cliente | 1 / 1 | `predict.py` · Aplicación web |
| **Total** | **5 / 5** | |

---

## 9. Conclusiones

1. **Amazon Rekognition Custom Labels** demostró ser una plataforma equivalente y competitiva frente a Azure Custom Vision para la tarea de clasificación de imágenes multiclase, con una experiencia de usuario clara y una API robusta.

2. La metodología **Spec Driven Design** facilitó la organización del proyecto, permitiendo establecer criterios de éxito medibles antes de la implementación y asegurando la trazabilidad con los requisitos académicos.

3. El **Transfer Learning** aplicado por AWS permitió obtener métricas satisfactorias de Precision y Recall con un dataset de apenas 51 imágenes, evidenciando el poder de los modelos pre-entrenados en escenarios con datos limitados.

4. La extensión del proyecto con una **aplicación web interactiva** enriqueció la entrega, demostrando la integración de un modelo de ML en un sistema de software real con consideraciones de costo (auto-apagado), seguridad (autenticación) y experiencia de usuario.

---

## 10. Referencias

- Amazon Web Services. (2024). *Amazon Rekognition Custom Labels Developer Guide*. https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/
- Boto3 Project. (2024). *Amazon Rekognition — AWS SDK for Python*. https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html
- FastAPI. (2024). *FastAPI Documentation*. https://fastapi.tiangolo.com
- Tan, M., & Le, Q. (2019). EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks. *ICML 2019*.

---

*Repositorio: [github.com/jmmana/Maestria-Vision-Computador-Clasificacion](https://github.com/jmmana/Maestria-Vision-Computador-Clasificacion)*  
*Proyecto académico — Universidad de La Salle · Maestría en Inteligencia Artificial · 2026*
