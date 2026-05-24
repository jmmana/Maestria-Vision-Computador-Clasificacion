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

def predecir(image_path: str, project_version_arn: str, region: str = "us-east-1",
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
        print(f"❌ Error: no se encontró la imagen '{image_path}'")
        sys.exit(1)

    print(f"\n🔍 Analizando imagen: {img.name}")
    print("─" * 40)

    # Leer imagen como bytes
    with open(img, "rb") as f:
        image_bytes = f.read()

    # Llamar a Rekognition
    client = boto3.client("rekognition", region_name=region)

    try:
        response = client.detect_custom_labels(
            ProjectVersionArn=project_version_arn,
            Image={"Bytes": image_bytes},
            MinConfidence=min_confidence,
        )
    except client.exceptions.ResourceNotReadyException:
        print("❌ El modelo no está en estado RUNNING.")
        print("   Asegúrate de haberlo iniciado en la consola de AWS.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al llamar a Rekognition: {e}")
        sys.exit(1)

    labels = response.get("CustomLabels", [])

    if not labels:
        print("⚠️  No se detectó ninguna clase con suficiente confianza.")
        print(f"   (umbral actual: {min_confidence}%)")
    else:
        # Ordenar por confianza descendente
        labels.sort(key=lambda x: x["Confidence"], reverse=True)
        top = labels[0]

        print(f"  Prediccion: {top['Name'].upper()}")
        print(f"   Confianza:  {top['Confidence']:.1f}%")

        if len(labels) > 1:
            print("\n📊 Todas las detecciones:")
            for lbl in labels:
                bar = "█" * int(lbl["Confidence"] / 5)
                print(f"   {lbl['Name']:12s} {lbl['Confidence']:5.1f}%  {bar}")

    print("─" * 40 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Argos — Clasificador de animales con AWS Rekognition Custom Labels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python predict.py --image foto_elefante.jpg --model-arn arn:aws:rekognition:...
  python predict.py --image lion.jpg --model-arn arn:aws:rekognition:... --min-confidence 70
        """
    )
    parser.add_argument("--image", required=True, help="Ruta de la imagen a clasificar")
    parser.add_argument("--model-arn", required=True,
                        help="ARN del modelo publicado en AWS Rekognition")
    parser.add_argument("--region", default="us-east-1", help="Región AWS (default: us-east-1)")
    parser.add_argument("--min-confidence", type=float, default=50.0,
                        help="Confianza mínima 0-100 (default: 50)")

    args = parser.parse_args()
    predecir(args.image, args.model_arn, args.region, args.min_confidence)


if __name__ == "__main__":
    main()
