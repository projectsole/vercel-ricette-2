#!/usr/bin/env python3
"""
Script per estrarre il testo da ogni pagina dei PDF e creare
un indice di ricerca (search_index.json) in ogni cartella di immagini.

Uso:
    python extract_text.py /percorso/alla/cartella/con/i/pdf

Lo script cerca tutti i file .pdf nella cartella indicata e,
per ciascuno, salva un file search_index.json nella corrispondente
cartella di immagini in static/images/.
"""

import json
import os
import sys

import pdfplumber


def extract_text_from_pdf(pdf_path):
    """Estrae il testo da ogni pagina del PDF."""
    pages = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages[str(i)] = text.strip()
    return pages


def main():
    if len(sys.argv) < 2:
        print("Uso: python extract_text.py /percorso/cartella/pdf")
        sys.exit(1)

    pdf_dir = sys.argv[1]
    if not os.path.isdir(pdf_dir):
        print(f"Errore: '{pdf_dir}' non è una cartella valida")
        sys.exit(1)

    # Cartella delle immagini nel progetto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "static", "images")

    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"Nessun PDF trovato in '{pdf_dir}'")
        sys.exit(1)

    for pdf_file in sorted(pdf_files):
        pdf_path = os.path.join(pdf_dir, pdf_file)
        # La cartella di immagini ha lo stesso nome del file PDF
        target_folder = os.path.join(images_dir, pdf_file)

        if not os.path.isdir(target_folder):
            print(f"⚠ Cartella immagini non trovata per '{pdf_file}', salto.")
            continue

        print(f"Elaboro: {pdf_file}...")
        pages = extract_text_from_pdf(pdf_path)

        output_path = os.path.join(target_folder, "search_index.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"pages": pages}, f, ensure_ascii=False, indent=2)

        non_empty = sum(1 for t in pages.values() if t)
        print(f"  → {len(pages)} pagine ({non_empty} con testo) → {output_path}")

    print("\nFatto! Indici di ricerca creati.")


if __name__ == "__main__":
    main()
