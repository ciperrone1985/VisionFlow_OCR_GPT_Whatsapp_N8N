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

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import io
import re #função repgex

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()


# Cria função para classificação de texto
def classifica_texto(texto: str) -> str: # função retorna uma string
    texto = texto.lower()
    
    match = re.search(r"cbbi.*?(\d{1,3})", texto)
    if not match:
        numeros = re.findall(r"\d{1,3}", texto)
        if numeros:
            valor_cbbi = int(numeros[0])
        else:
            return "valor cbbi não identificado"
    else:
        valor_cbbi = int(match.group(1))
        
     
    if 0 <= valor_cbbi <= 25:
        return "Zona de oportunidade - possível fundo de ciclo"
    elif 26 <= valor_cbbi <= 50:
        return "Fase de acumulação - Lateralidade ou início de recuperação"
    elif 51<= valor_cbbi <=75:
        return "Alerta de valorização - preço em alta"
    elif 76 <= valor_cbbi <=90:
        return "Zona de perigo - sinais de euforia"
    elif 91 <= valor_cbbi <= 100:
        return"Provável topo de ciclo - confiança extrema de topo"

    
    ''' if "at the peak" in texto or "top" in texto or "máximo" in texto:
        return "Provável topo de ciclo"
    elif "undervalued" in texto or "cheap" in texto or "abaixo do valor" in texto:
        return"Zona de oportunidade"
    elif "bottom" in texto or "low" in texto or "mínimo" in texto:
        return "Sem classificação clara"'''

@app.post("/analisa")
async def analisa(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        texto_extraido = pytesseract.image_to_string(image, lang="eng+por")
        classificacao = classifica_texto(texto_extraido)
        return {
            "text_extraido": texto_extraido.strip(),
            "classificacao": classificacao
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})
