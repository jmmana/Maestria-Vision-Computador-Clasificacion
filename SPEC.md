# SPEC — Argos: Clasificador de Imágenes de Animales

> **Spec Driven Design** — Este documento define el QUÉ antes del CÓMO.  
> Todo el código, infraestructura y documentación se deriva de esta especificación.

---

## 1. Problema

Clasificar automáticamente imágenes de animales salvajes africanos en tres categorías:
`elephant`, `giraffe`, `lion`.

**Caso de uso:** Aplicación de identificación de fauna para guías de safari, investigadores
y entusiastas de la naturaleza.

---

## 2. Autores

| Nombre | Rol |
|--------|-----|
| María Alejandra Gómez Piedrahita | Investigadora principal |
| Juan Manuel Castillo Pinto | Arquitecto de solución |

**Materia:** 2026-1 · VISIÓN POR COMPUTADOR · G02  
**Universidad:** La Salle — Maestría en Inteligencia Artificial  
**Actividad:** 4 — Unidad 2: Técnicas de entrenamiento y optimización

---

## 3. Alcance

### 3.1 En scope
- Clasificación multiclase (1 etiqueta por imagen)
- 3 clases: `elephant`, `giraffe`, `lion`
- Entrenamiento en AWS Rekognition Custom Labels
- API REST de predicción publicada en AWS
- Cliente Python para pruebas desde línea de comandos
- Métricas: Precision y Recall por clase

### 3.2 Fuera de scope
- Detección de objetos (bounding boxes)
- Tiempo real / video
- Clases adicionales de animales
- Despliegue en producción

---

## 4. Dataset

| Atributo | Valor |
|----------|-------|
| Total imágenes | 51 |
| Clases | 3 |
| Imágenes por clase | 17 |
| Formato | JPG |
| Split | 80% train / 20% test (automático) |
| Fuente | Dataset proporcionado por el docente |

### Distribución
```
data/training/
├── elephant/   → 17 imágenes
├── giraffe/    → 17 imágenes
└── lion/       → 17 imágenes
```

---

## 5. Criterios de éxito

| Métrica | Mínimo aceptable | Objetivo |
|---------|-----------------|---------|
| Precision global | 70% | ≥ 85% |
| Recall global | 70% | ≥ 85% |
| Prueba manual (5 imgs) | 3/5 correctas | 5/5 correctas |

---

## 6. Arquitectura de la solución

```
[Imágenes locales]
       │
       ▼
[AWS Rekognition Custom Labels]
  ├── Proyecto: Argos
  ├── Dataset: training (80/20 split automático)
  ├── Entrenamiento: Quick Training
  └── Modelo publicado → ARN endpoint
       │
       ▼
[Cliente Python: predict.py]
  └── Input: imagen local
  └── Output: clase + confianza (%)
```

---

## 7. API de predicción

**Servicio:** AWS Rekognition `detect_custom_labels`

```python
# Request
{
  "ProjectVersionArn": "<ARN del modelo publicado>",
  "Image": {"Bytes": <imagen_bytes>},
  "MinConfidence": 50
}

# Response esperado
{
  "CustomLabels": [
    {"Name": "elephant", "Confidence": 94.5}
  ]
}
```

---

## 8. Infraestructura AWS

| Recurso | Nombre | Región |
|---------|--------|--------|
| Rekognition Custom Labels | Argos | us-east-1 |
| Proyecto | Argos | — |
| Dataset | argos-training | — |

---

## 9. Entregables

- [ ] `README.md` — Documentación completa del proyecto
- [ ] `SPEC.md` — Este documento (especificación)
- [ ] `src/client/predict.py` — App cliente CLI
- [ ] `src/utils/upload_dataset.py` — Script de carga a AWS
- [ ] `docs/training_results.md` — Métricas post-entrenamiento
- [ ] `docs/screenshots/` — Evidencia del proceso en AWS
- [ ] `informe/informe_actividad4.md` — Informe académico
- [ ] PDF del informe con capturas de pantalla

---

## 10. Riesgos

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|------------|
| Dataset pequeño (17 imgs/clase) | Alta | Usar Quick Training + data augmentation |
| Costo AWS | Baja | Créditos universitarios + detener modelo post-prueba |
| Similitud visual entre clases | Media | Revisar imágenes diversas por clase |
