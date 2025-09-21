#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def main():
    print("=== RELLENADOR DE CONFIGURACION.JSON ===")
    
    # Contenido que vamos a escribir
    configuracion = {
        "porcentajeBeneficio": 15,
        "costes": {
            "Manzana": 2.5,
            "Banana": 1.5,
            "Naranja": 2.0,
            "Pera": 1.0,
            "Uva": 3.0
        },
        "costeDecisiones": {
            "Decisión A": 5,
            "Decisión B": 10,
            "Decisión C": 15,
            "Decisión D": 20
        }
    }
    
    archivo = "configuracion.json"
    
    print(f"📁 Intentando escribir en: {os.path.abspath(archivo)}")
    
    try:
        # Método 1: Escribir directamente
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(configuracion, f, indent=2, ensure_ascii=False)
        print("✅ Método 1: Escrito con json.dump")
        
        # Verificar que se escribió
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        
        if contenido:
            print(f"📝 Archivo tiene {len(contenido)} caracteres")
            print("📋 Contenido:")
            print(contenido)
        else:
            print("❌ El archivo sigue vacío después de escribir")
            
            # Método 2: Escribir como texto plano
            texto_json = """{
  "porcentajeBeneficio": 15,
  "costes": {
    "Manzana": 2.5,
    "Banana": 1.5,
    "Naranja": 2.0,
    "Pera": 1.0,
    "Uva": 3.0
  },
  "costeDecisiones": {
    "Decisión A": 5,
    "Decisión B": 10,
    "Decisión C": 15,
    "Decisión D": 20
  }
}"""
            
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(texto_json)
            print("✅ Método 2: Escrito como texto plano")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("=== FIN ===")

if __name__ == "__main__":
    main()