# Estado del proyecto Argos — Punto de retoma

**Última actualización:** 25 de mayo de 2026  
**Entregado por:** Juan Manuel Castillo Pinto + María Alejandra Gómez Piedrahita

---

## ✅ Qué está completamente terminado

| Componente | Estado | Detalle |
|------------|--------|---------|
| Modelo AWS Rekognition | ✅ Entrenado | Quick Training completado, métricas en AWS Console |
| Dataset | ✅ Subido | 51 imágenes · 17 por clase (elephant, giraffe, lion) |
| Cliente CLI | ✅ Funcional | `src/client/predict.py` con boto3 |
| App web | ✅ En producción | https://argos.warlockcode.com |
| Informe PDF | ✅ Generado | `informe/Informe_Argos_Actividad4_v2.pdf` (6.5 MB · 17 figuras) |
| GitHub | ✅ Actualizado | https://github.com/jmmana/Maestria-Vision-Computador-Clasificacion |
| Despliegue Coolify | ✅ Activo | Proyecto: Maestria · App: Argos |

---

## 🔑 Credenciales y accesos

| Recurso | Dato |
|---------|------|
| App web URL | https://argos.warlockcode.com |
| Usuario app | `admin` |
| Contraseña app | `argos2026lasalle` |
| AWS Region | `us-east-1` |
| AWS Account ID | `442444704156` |
| Project ARN | `arn:aws:rekognition:us-east-1:442444704156:project/Argos/1779659669813` |
| Model ARN | `arn:aws:rekognition:us-east-1:442444704156:project/Argos/version/Argos.2026-05-24T18.36.39/1779665799778` |
| Coolify URL | https://coolify.warlockcode.com |
| Coolify App UUID | `hhn9vsvr85ic9s0bjm9x0tnb` |
| GitHub repo | https://github.com/jmmana/Maestria-Vision-Computador-Clasificacion |

---

## ⚠️ Cosas importantes a saber

### El modelo AWS cobra mientras está encendido
- Costo aproximado: **~$4 USD/hora** cuando está en estado RUNNING
- El auto-apagado en la app funciona a los **60 minutos**
- Si no usas la app, verificar en AWS Console que el modelo esté STOPPED
- Para apagarlo manualmente desde CLI:
  ```bash
  aws rekognition stop-project-version \
    --project-version-arn "arn:aws:rekognition:us-east-1:442444704156:project/Argos/version/Argos.2026-05-24T18.36.39/1779665799778" \
    --region us-east-1
  ```

### Bug resuelto — Project ARN
El project ARN real es `project/Argos/1779659669813` (con sufijo numérico).  
El código en `web/main.py` lo resuelve automáticamente con `describe_projects()` y lo cachea en memoria.  
No modificar esta lógica o el estado volverá a mostrar UNKNOWN.

---

## 📋 Tareas pendientes (si se retoma)

| Tarea | Prioridad | Detalle |
|-------|-----------|---------|
| Llenar métricas reales | Media | En `docs/training_results.md` están como placeholders. Ver valores reales en AWS Console → proyecto Argos → modelo → pestaña Evaluation |
| Nombre del docente | Baja | `Informe.md` línea 15: `(nombre del docente)` — reemplazar y regenerar PDF |
| Regenerar PDF final | Baja | Después de completar lo anterior: `python3 /tmp/generar_pdf_v2.py` |
| Screenshots adicionales | Opcional | Quick Test en AWS Console (clasificación directa desde AWS) |

---

## 📁 Estructura de archivos clave

```
Argos/
├── Informe.md                          ← Documento fuente del informe (editar aquí)
├── README.md                           ← Documentación GitHub estilo publicación
│
├── informe/
│   └── Informe_Argos_Actividad4_v2.pdf ← PDF entregable (6.5 MB)
│
├── src/client/
│   └── predict.py                      ← Cliente CLI para clasificar imágenes
│
├── web/
│   ├── main.py                         ← Backend FastAPI (API + lógica AWS)
│   ├── Dockerfile                      ← Containerización
│   └── templates/
│       ├── index.html                  ← Landing + login
│       └── dashboard.html              ← Clasificador interactivo
│
└── docs/
    ├── ESTADO_PROYECTO.md              ← Este archivo
    ├── MANUAL_AWS.md                   ← Paso a paso del proceso en AWS
    ├── training_results.md             ← Métricas (completar con valores reales)
    └── screenshots/                    ← 20+ capturas del proceso completo
```

---

## 🔄 Cómo regenerar el PDF

```bash
cd ~/Documents/Maestria/VisionPorComputador/Argos
python3 /tmp/generar_pdf_v2.py
# Genera: informe/Informe_Argos_Actividad4_v2.pdf
```

Requiere: `pip install markdown weasyprint`

---

## 🚀 Cómo redesplegar la app

```bash
# Opción 1: Push a GitHub (Coolify detecta el cambio automáticamente)
git push origin main

# Opción 2: Redeploy manual via API Coolify
COOLIFY_TOKEN="4|2QCLv9fwHpdF2YAMe8guiVu790VKMKqMfOXnC4sT0db6135a"
curl -X POST "https://coolify.warlockcode.com/api/v1/applications/hhn9vsvr85ic9s0bjm9x0tnb/start" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"
```

---

## 📊 Métricas del modelo (ver en AWS Console para valores reales)

Ir a: **AWS Console → Rekognition → Custom Labels → Argos → Versión entrenada → Evaluation**

Las métricas están capturadas en `docs/screenshots/Evaluacion del modelo.png`.

---

*Documento generado al cierre del proyecto · Actividad 4 · Visión por Computador · La Salle 2026*
