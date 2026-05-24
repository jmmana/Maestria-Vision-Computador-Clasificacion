# Argos — Clasificador de Imágenes de Animales Salvajes

> *Argos Panoptes: el gigante de cien ojos de la mitología griega que todo lo veía.*  
> *Para un modelo de visión por computador, un nombre perfecto.*

[![AWS Rekognition](https://img.shields.io/badge/AWS-Rekognition%20Custom%20Labels-FF9900?logo=amazon-aws)](https://aws.amazon.com/rekognition/custom-labels-features/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Universidad La Salle](https://img.shields.io/badge/La%20Salle-Maestría%20IA-004B87)](https://www.lasalle.edu.co)

---

## 👥 Autores

| Nombre | Rol |
|--------|-----|
| **María Alejandra Gómez Piedrahita** | Investigadora principal |
| **Juan Manuel Castillo Pinto** | Arquitecto de solución |

**Materia:** 2026-1 · VISIÓN POR COMPUTADOR · G02  
**Actividad:** 4 — Unidad 2: Técnicas de entrenamiento y optimización para modelos de visión por computador  
**Universidad:** La Salle — Maestría en Inteligencia Artificial

---

## 🎯 ¿Qué hace Argos?

Argos es un modelo de clasificación de imágenes entrenado en **AWS Rekognition Custom Labels** capaz de identificar automáticamente tres animales salvajes africanos:

| Clase | Animal | Imágenes de entrenamiento |
|-------|--------|--------------------------|
| `elephant` | Elefante africano | 17 |
| `giraffe` | Jirafa | 17 |
| `lion` | León | 17 |

---

## 🏗️ Arquitectura

```mermaid
flowchart TD
    A[📁 Dataset Local\n51 imágenes\n3 clases] --> B[☁️ AWS Rekognition\nCustom Labels]
    B --> C{Proyecto Argos}
    C --> D[📊 Dataset de entrenamiento\n80% train / 20% test]
    D --> E[🧠 Entrenamiento\nQuick Training]
    E --> F[📈 Evaluación\nPrecision & Recall]
    F --> G{¿Métricas OK?}
    G -- Sí --> H[🚀 Publicar Modelo\nEndpoint ARN]
    G -- No --> D
    H --> I[🐍 Cliente Python\npredict.py]
    I --> J[🖼️ Imagen de prueba] 
    J --> K[✅ Predicción\nClase + Confianza %]

    style A fill:#f0f4ff,stroke:#4a6cf7
    style B fill:#FF9900,color:#fff,stroke:#FF9900
    style H fill:#00a651,color:#fff,stroke:#00a651
    style K fill:#00a651,color:#fff,stroke:#00a651
```

---

## 🔄 Flujo del proyecto (Spec Driven Design)

```mermaid
gantt
    title Argos — Flujo de implementación
    dateFormat  YYYY-MM-DD
    section Especificación
    SPEC.md — Definición del problema    :done, spec, 2026-05-24, 1d
    section Datos
    Dataset local (51 imgs)              :done, data, 2026-05-24, 1d
    section AWS
    Crear proyecto Rekognition           :done, aws1, 2026-05-24, 1d
    Subir y etiquetar imágenes           :active, aws2, 2026-05-24, 1d
    Quick Training (~45 min)             :aws3, after aws2, 1d
    Evaluar métricas                     :aws4, after aws3, 1d
    Publicar modelo                      :aws5, after aws4, 1d
    section Cliente
    predict.py — App cliente CLI         :cli, 2026-05-24, 1d
    section Entrega
    Informe PDF                          :informe, after aws5, 1d
```

---

## 📁 Estructura del proyecto

```
Argos/
├── README.md                    # Este archivo
├── SPEC.md                      # Especificación Spec Driven Design
├── .gitignore
│
├── data/
│   ├── training/
│   │   ├── elephant/            # 17 imágenes de elefantes
│   │   ├── giraffe/             # 17 imágenes de jirafas
│   │   └── lion/                # 17 imágenes de leones
│   └── test/                    # Imágenes para prueba del cliente
│
├── src/
│   ├── client/
│   │   └── predict.py           # 🐍 App cliente — prueba el modelo
│   └── utils/
│       └── upload_dataset.py    # Utilidades de carga
│
├── docs/
│   ├── training_results.md      # Métricas post-entrenamiento
│   ├── architecture.md          # Decisiones de arquitectura
│   └── screenshots/             # Evidencia del proceso AWS
│
└── informe/
    └── informe_actividad4.md    # Informe académico
```

---

## 🚀 Guía de reproducción paso a paso

### Prerrequisitos

```bash
pip install boto3 pillow
aws configure  # Configurar credenciales AWS
```

### 1. Clonar el repositorio

```bash
git clone https://github.com/jmmana/Maestria-Vision-Computador-Clasificacion.git
cd Argos
```

### 2. Configurar AWS CLI

```bash
aws configure
# AWS Access Key ID: <tu-key>
# AWS Secret Access Key: <tu-secret>
# Default region: us-east-1
# Output format: json
```

### 3. Subir el modelo y predecir

```bash
# Prueba de predicción (una vez publicado el modelo)
python src/client/predict.py \
  --image data/test/mi_animal.jpg \
  --project-arn <ARN-del-proyecto> \
  --model-arn <ARN-del-modelo>
```

### Ejemplo de salida

```
🔍 Analizando imagen: mi_animal.jpg
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Predicción: ELEPHANT
   Confianza: 94.7%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📸 Proceso de implementación en AWS

### 1. Crear conjunto de datos
![Crear conjunto de datos](docs/screenshots/Crear%20Conjunto%20de%20datos.png)

### 2. Configuración 80% entrenamiento / 20% prueba
![Configuración 80/20](docs/screenshots/Modeo%20de%20formacion%2080%20.png)

### 3. Agregar imágenes al conjunto de datos
![Agregar imágenes](docs/screenshots/Agregar%20imagenes%20al%20conjunto%20de%20datos.png)

### 4. Crear etiquetas (elephant · giraffe · lion)
![Crear etiquetas](docs/screenshots/Crear%20Etiquetas%20para%20el%20conjunto%20de%20datos.png)

### 5. Dataset completo — 17 imágenes por categoría
![Imágenes etiquetadas](docs/screenshots/Imagenes%20Etiquedatas%2017%20por%20categorias.png)

### 6. Detalle del conjunto de datos
![Detalle dataset](docs/screenshots/Detalle%20del%20conjunto%20de%20datos.png)

### 7. Configuración del modelo de entrenamiento
![Modelo de entrenamiento](docs/screenshots/Modelo%20de%20entrenamiento.png)

### 8. Entrenamiento en progreso
![Entrenamiento en progreso](docs/screenshots/Modelo%20en%20entrenamiento.png)

> Ver el manual completo en [`docs/MANUAL_AWS.md`](docs/MANUAL_AWS.md)

---

## 📊 Resultados del modelo

> 📝 *Esta sección se completa después del entrenamiento.*  
> Ver [`docs/training_results.md`](docs/training_results.md) para las métricas completas.

| Clase | Precision | Recall | F1 |
|-------|-----------|--------|----|
| Elephant | — | — | — |
| Giraffe | — | — | — |
| Lion | — | — | — |
| **Promedio** | — | — | — |

---

## ☁️ Infraestructura AWS

```mermaid
graph LR
    subgraph AWS["☁️ AWS — us-east-1"]
        RC[Rekognition\nCustom Labels]
        PR[Proyecto: Argos]
        DS[Dataset:\nargos-training]
        MV[Modelo v1\nPublicado]
        EP[Endpoint\nPredicción]
    end
    
    LOCAL[💻 Local\ndata/training/] --> DS
    DS --> PR
    PR --> MV
    MV --> EP
    EP --> CLI[🐍 predict.py]

    style AWS fill:#fff3e0,stroke:#FF9900
    style MV fill:#00a651,color:#fff
    style EP fill:#00a651,color:#fff
```

---

## 📋 Criterios de evaluación

| Criterio | Puntos | Estado |
|----------|--------|--------|
| Creación y configuración del recurso AWS AI Services | 1 | ✅ |
| Creación y configuración del proyecto Custom Labels | 2 | ✅ |
| Entrenamiento y evaluación del modelo | 1 | ⏳ |
| Publicar y probar con app cliente | 1 | ⏳ |
| **Total** | **5** | |

---

## 📚 Referencias

- [Amazon Rekognition Custom Labels — Documentación oficial](https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/what-is.html)
- [Boto3 Rekognition — SDK Python](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html)
- [Dataset de animales](data/training/)

---

## 📄 Licencia

Proyecto académico — La Salle, Maestría en Inteligencia Artificial, 2026.
