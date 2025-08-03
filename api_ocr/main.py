# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 18:30:17 2025
Faz api http com fastapi

necessário instalar as bibiliotecas:
    fastapi uvicorn -> pip install fastapi uvicorn
    PIL
    pytesseract
    io
    pip install python-multipart
    
    necessário instalar https://github.com/UB-Mannheim/tesseract/wiki e adicionar o caminho da 
    instalação nas variáveis de ambiente -> C:\Program Files\Tesseract-OCR
@author: perro
"""

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import io

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.post("/analisa")
async def analisa(file: UploadFile):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    texto = pytesseract.image_to_string(image)
    return {"resultado": texto}
    