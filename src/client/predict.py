#!/usr/bin/env python3
"""
Argos — Cliente de predicción para AWS Rekognition Custom Labels
Actividad 4: Clasificación de imágenes de animales

Autores:
  - María Alejandra Gómez Piedrahita
  - Juan Manuel Castillo Pinto

Materia: 2026-1 · VISIÓN POR COMPUTADOR · G02
Universidad La Salle — Maestría en IA
"""

import argparse
import sys
import boto3
from pathlib import Path

# ARN del modelo publicado en AWS
MODEL_ARN = "arn:aws:rekognition:us-east-1:442444704156:project/Argos/version/Argos.2026-05-24T18.36.39/1779665799778"
REGION = "us-east-1"


def predecir(image_path: str, project_version_arn: str, region: str = REGION,
             min_confidence: float = 50.0) -> None:
    """
    Envía una imagen al modelo Argos en AWS y muestra la predicción.

    Args:
        image_path: Ruta local de la imagen a clasificar
        project_version_arn: ARN del modelo publicado en Rekognition
        region: Región AWS (default: us-east-1)
        min_confidence: Confianza mínima para reportar un resultado (default: 50%)
    """
    img = Path(image_path)
    if not img.exists():
        print(f"Error: no se encontró la imagen '{image_path}'")
        sys.exit(1)

    print(f"\nAnalizando imagen: {img.name}")
    print("-" * 40)

    with open(img, "rb") as f:
        image_bytes = f.read()

    client = boto3.client("rekognition", region_name=region)

    try:
        response = client.detect_custom_labels(
            ProjectVersionArn=project_version_arn,
            Image={"Bytes": image_bytes},
            MinConfidence=min_confidence,
        )
    except client.exceptions.ResourceNotReadyException:
        print("Error: El modelo no está en estado RUNNING.")
        print("Ejecuta primero: python predict.py --start-model")
        sys.exit(1)
    except Exception as e:
        print(f"Error al llamar a Rekognition: {e}")
        sys.exit(1)

    labels = response.get("CustomLabels", [])

    if not labels:
        print("No se detectó ninguna clase con suficiente confianza.")
        print(f"Umbral actual: {min_confidence}%")
    else:
        labels.sort(key=lambda x: x["Confidence"], reverse=True)
        top = labels[0]
        print(f"Prediccion : {top['Name'].upper()}")
        print(f"Confianza  : {top['Confidence']:.1f}%")

        if len(labels) > 1:
            print("\nTodas las detecciones:")
            for lbl in labels:
                bar = "#" * int(lbl["Confidence"] / 5)
                print(f"  {lbl['Name']:12s} {lbl['Confidence']:5.1f}%  {bar}")

    print("-" * 40 + "\n")


def iniciar_modelo(project_version_arn: str, region: str = REGION) -> None:
    """Inicia el modelo en AWS (necesario antes de predecir)."""
    client = boto3.client("rekognition", region_name=region)
    print(f"Iniciando modelo...")
    client.start_project_version(
        ProjectVersionArn=project_version_arn,
        MinInferenceUnits=1
    )
    print("Modelo iniciado. Espera 2-3 minutos a que quede en estado RUNNING.")
    print(f"Verifica en: https://us-east-1.console.aws.amazon.com/rekognition/custom-labels")


def detener_modelo(project_version_arn: str, region: str = REGION) -> None:
    """Detiene el modelo en AWS (para evitar costos)."""
    client = boto3.client("rekognition", region_name=region)
    client.stop_project_version(ProjectVersionArn=project_version_arn)
    print("Modelo detenido. Ya no genera costos.")


def main():
    parser = argparse.ArgumentParser(
        description="Argos — Clasificador de animales con AWS Rekognition Custom Labels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Ejemplos:
  # Iniciar el modelo (una vez, antes de predecir)
  python predict.py --start-model

  # Clasificar una imagen
  python predict.py --image foto.jpg

  # Detener el modelo (al terminar, para evitar costos)
  python predict.py --stop-model

Model ARN: {MODEL_ARN}
        """
    )
    parser.add_argument("--image", help="Ruta de la imagen a clasificar")
    parser.add_argument("--model-arn", default=MODEL_ARN, help="ARN del modelo (opcional, ya está configurado)")
    parser.add_argument("--region", default=REGION, help="Región AWS")
    parser.add_argument("--min-confidence", type=float, default=50.0, help="Confianza mínima 0-100")
    parser.add_argument("--start-model", action="store_true", help="Iniciar el modelo en AWS")
    parser.add_argument("--stop-model", action="store_true", help="Detener el modelo en AWS")

    args = parser.parse_args()

    if args.start_model:
        iniciar_modelo(args.model_arn, args.region)
    elif args.stop_model:
        detener_modelo(args.model_arn, args.region)
    elif args.image:
        predecir(args.image, args.model_arn, args.region, args.min_confidence)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
