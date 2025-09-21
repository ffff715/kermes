import json
import os

# Configuración por defecto
configuracion_defecto = {
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

# Ruta del archivo JSON
archivo_config = "configuracion.json"

try:
    # Escribir el archivo JSON
    with open(archivo_config, 'w', encoding='utf-8') as archivo:
        json.dump(configuracion_defecto, archivo, indent=2, ensure_ascii=False)
    
    print("✅ Archivo configuracion.json creado exitosamente")
    print("📋 Contenido:")
    print(json.dumps(configuracion_defecto, indent=2, ensure_ascii=False))
    
    # Verificar que se escribió correctamente
    with open(archivo_config, 'r', encoding='utf-8') as archivo:
        verificacion = json.load(archivo)
    
    print("✅ Verificación: El archivo se leyó correctamente")
    print(f"📊 Porcentaje de beneficio: {verificacion['porcentajeBeneficio']}%")
    print(f"🍎 Productos configurados: {len(verificacion['costes'])}")
    print(f"🎯 Decisiones configuradas: {len(verificacion['costeDecisiones'])}")

except Exception as e:
    print(f"❌ Error al crear el archivo: {e}")

input("\nPresiona Enter para cerrar...")