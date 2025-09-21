import json
import sys
import os

print("🔧 Script para forzar creación de configuracion.json")
print("📁 Directorio actual:", os.getcwd())

# Datos a escribir
datos = {
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

# Ruta completa del archivo
ruta_archivo = "configuracion.json"

try:
    # Borrar archivo si existe
    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)
        print("🗑️ Archivo anterior eliminado")
    
    # Escribir nuevo archivo
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    print("✅ Archivo escrito")
    
    # Verificar inmediatamente
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        print(f"📄 Tamaño del archivo: {len(contenido)} caracteres")
        print("📋 Primeros 100 caracteres:")
        print(contenido[:100])
    else:
        print("❌ El archivo no se creó")

except Exception as e:
    print(f"❌ Error: {e}")
    print(f"❌ Tipo de error: {type(e)}")

print("✅ Script terminado")