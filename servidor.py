#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde el HTML

# Archivos de datos
ARCHIVO_CONFIG = "configuracion.json"
ARCHIVO_VENTAS = "ventas.json"

def asegurar_archivos():
    """Crear archivos si no existen"""
    
    # Configuración por defecto
    config_defecto = {
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
    
    # Crear configuración.json si no existe o está vacío
    if not os.path.exists(ARCHIVO_CONFIG) or os.path.getsize(ARCHIVO_CONFIG) == 0:
        with open(ARCHIVO_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config_defecto, f, indent=2, ensure_ascii=False)
        print(f"✅ Creado {ARCHIVO_CONFIG}")
    
    # Crear ventas.json si no existe
    if not os.path.exists(ARCHIVO_VENTAS):
        with open(ARCHIVO_VENTAS, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2, ensure_ascii=False)
        print(f"✅ Creado {ARCHIVO_VENTAS}")

def cargar_configuracion():
    """Cargar configuración desde JSON"""
    try:
        with open(ARCHIVO_CONFIG, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        asegurar_archivos()
        with open(ARCHIVO_CONFIG, 'r', encoding='utf-8') as f:
            return json.load(f)

def guardar_configuracion(config):
    """Guardar configuración en JSON"""
    with open(ARCHIVO_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def cargar_ventas():
    """Cargar ventas desde JSON"""
    try:
        with open(ARCHIVO_VENTAS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def guardar_ventas(ventas):
    """Guardar ventas en JSON"""
    with open(ARCHIVO_VENTAS, 'w', encoding='utf-8') as f:
        json.dump(ventas, f, indent=2, ensure_ascii=False)

# === RUTAS DE LA API ===

@app.route('/')
def inicio():
    """Página principal"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def archivos_estaticos(filename):
    """Servir archivos estáticos"""
    return send_from_directory('.', filename)

@app.route('/api/configuracion', methods=['GET'])
def obtener_configuracion():
    """Obtener configuración actual"""
    config = cargar_configuracion()
    return jsonify(config)

@app.route('/api/configuracion', methods=['POST'])
def actualizar_configuracion():
    """Actualizar configuración"""
    try:
        nueva_config = request.json
        guardar_configuracion(nueva_config)
        return jsonify({"success": True, "message": "Configuración actualizada"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    """Obtener datos de productos y ventas"""
    try:
        # Datos de productos (casillas)
        datos = {
            "ventas": cargar_ventas(),
            "casillas": [
                {"nombre": "Manzana", "valor": 5.3},
                {"nombre": "Banana", "valor": 3},
                {"nombre": "Naranja", "valor": 4},
                {"nombre": "Pera", "valor": 2},
                {"nombre": "Uva", "valor": 6}
            ]
        }
        return jsonify(datos)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/ventas', methods=['GET'])
def obtener_ventas():
    """Obtener todas las ventas"""
    ventas = cargar_ventas()
    return jsonify(ventas)

@app.route('/api/ventas', methods=['POST'])
def nueva_venta():
    """Registrar nueva venta"""
    try:
        datos_venta = request.json
        print(f"📥 Datos recibidos: {datos_venta}")
        
        if not datos_venta:
            print("❌ No se recibieron datos")
            return jsonify({"success": False, "message": "No se recibieron datos"}), 400
        
        # Validar estructura de datos nueva vs antigua
        es_sistema_nuevo = 'categoria' in datos_venta and 'producto' in datos_venta
        
        if es_sistema_nuevo:
            # Sistema nuevo: validar campos requeridos
            campos_requeridos = ['categoria', 'producto', 'emoji', 'precioFinal', 'tipo']
            for campo in campos_requeridos:
                if campo not in datos_venta:
                    print(f"❌ Campo requerido faltante: {campo}")
                    return jsonify({"success": False, "message": f"Campo requerido faltante: {campo}"}), 400
            
            # Añadir timestamp si no existe
            if 'fecha' not in datos_venta:
                datos_venta['fecha'] = datetime.now().isoformat()
        else:
            # Sistema antiguo: usar timestamp actual
            datos_venta['fecha'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        # Cargar ventas existentes
        ventas = cargar_ventas()
        ventas.append(datos_venta)
        
        # Guardar
        guardar_ventas(ventas)
        
        producto_info = datos_venta.get('producto', datos_venta.get('total', 'Desconocido'))
        print(f"✅ Nueva venta registrada: {producto_info}")
        
        return jsonify({"success": True, "message": "Venta registrada", "id": len(ventas)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/ventas', methods=['DELETE'])
def borrar_todas_ventas():
    """Borrar todas las ventas"""
    try:
        guardar_ventas([])
        print("🗑️ Todas las ventas han sido borradas")
        return jsonify({"success": True, "message": "Todas las ventas borradas"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/ventas/borrar', methods=['DELETE'])
def borrar_ventas():
    """Borrar todas las ventas"""
    try:
        guardar_ventas([])
        return jsonify({"success": True, "message": "Ventas borradas"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/reset', methods=['POST'])
def reset_sistema():
    """Resetear todo el sistema"""
    try:
        # Borrar archivos existentes
        for archivo in [ARCHIVO_CONFIG, ARCHIVO_VENTAS]:
            if os.path.exists(archivo):
                os.remove(archivo)
        
        # Recrear archivos
        asegurar_archivos()
        
        return jsonify({"success": True, "message": "Sistema reseteado"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/estado', methods=['GET'])
def estado_sistema():
    """Obtener estado del sistema"""
    try:
        config = cargar_configuracion()
        ventas = cargar_ventas()
        
        estado = {
            "configuracion_ok": bool(config),
            "total_ventas": len(ventas),
            "archivos": {
                "configuracion": os.path.exists(ARCHIVO_CONFIG),
                "ventas": os.path.exists(ARCHIVO_VENTAS)
            }
        }
        
        return jsonify(estado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor Python para el sistema de ventas...")
    print("📁 Verificando archivos...")
    
    # Asegurar que existen los archivos
    asegurar_archivos()
    
    print("✅ Archivos verificados")
    print("🌐 Servidor disponible en: http://localhost:5001")
    print("📱 Abre: http://localhost:5001 para usar el sistema")
    print("🛑 Presiona Ctrl+C para detener")
    
    try:
        # Iniciar servidor en puerto 5001
        app.run(debug=False, host='localhost', port=5001, threaded=True)
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")
        print("💡 Intentando en puerto 5002...")
        try:
            app.run(debug=False, host='localhost', port=5002, threaded=True)
        except Exception as e2:
            print(f"❌ Error al iniciar en puerto 5002: {e2}")
            print("💡 Usa otro puerto o cierra aplicaciones que usen estos puertos")