# 🛒 Sistema de Ventas con Decisiones

## 📋 Descripción
Sistema web completo para gestionar ventas con:
- ✅ Selección de productos con checkboxes
- 🎯 Botones de decisión con costes
- 💰 Cálculo automático con porcentaje extra en euros
- 🔐 Dashboard protegido por contraseña
- 📊 Estadísticas completas (media, mediana, moda, desviación estándar)
- 🌐 **Funciona tanto en desarrollo local como en servidor remoto**

## 🚀 Instalación en tu Servidor

### Opción 1: Hosting con PHP (Recomendado)
**Compatible con:** cPanel, Hostinger, GoDaddy, SiteGround, etc.

1. **Subir archivos** - Copia todos los archivos a tu hosting:
   ```
   index.html
   opciones.html
   ventas.html
   script.js
   style.css
   api.php          ← ¡IMPORTANTE!
   .htaccess        ← Para Apache
   ```

2. **Verificar PHP** - Asegúrate de que tu hosting tenga PHP 7.0+

3. **Configurar permisos** - Los archivos JSON se crearán automáticamente

4. **¡Listo!** - Accede a `https://tudominio.com/index.html`

### Opción 2: Servidor con Python
**Compatible con:** VPS, servidores dedicados

1. **Instalar dependencias:**
   ```bash
   pip install flask flask-cors
   ```

2. **Subir archivos** y ejecutar:
   ```bash
   python servidor.py
   ```

3. **Acceder** via `http://tuservidor:5000/index.html`

## 🔧 Configuración Automática

El sistema **detecta automáticamente** dónde está ejecutándose:

- **🏠 Localhost:** Usa servidor Python (puerto 5000)
- **🌐 Servidor remoto:** Usa API PHP (`api.php`)

¡No necesitas cambiar ningún código!

## 📁 Estructura de Archivos

```
proyecto/
├── 📄 index.html          # Página principal
├── 📄 opciones.html       # Interface de ventas
├── 📄 ventas.html         # Dashboard admin
├── 📄 script.js           # Lógica principal
├── 📄 style.css           # Estilos
├── 🐘 api.php             # API para hosting PHP
├── 🐍 servidor.py         # Servidor Python (desarrollo)
├── ⚙️ .htaccess          # Configuración Apache
├── ⚙️ nginx.conf.example  # Configuración Nginx
├── 📊 configuracion.json  # Se crea automáticamente
└── 📊 datos.json          # Se crea automáticamente
```

## 🔐 Acceso al Dashboard

- **URL:** `tudominio.com/ventas.html`
- **Contraseña:** `admin123`
- **Función:** Ver estadísticas, exportar datos, ajustar porcentajes

## 📊 Archivos de Datos

### `configuracion.json`
```json
{
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
```

### `datos.json`
```json
{
  "ventas": [
    {
      "fecha": "2025-09-21 14:30:15",
      "casillas": [
        {"nombre": "Manzana", "valor": 5.3},
        {"nombre": "Banana", "valor": 3}
      ],
      "decision": {"nombre": "Decisión A (5 €)", "valor": 5},
      "subtotal": 8.3,
      "extra": 1.25,
      "total": 14.55
    }
  ]
}
```

## 🛠️ API Endpoints

### GET `/api.php/configuracion`
Obtener configuración actual

### POST `/api.php/configuracion`
Actualizar configuración

### GET `/api.php/datos`
Obtener todas las ventas

### POST `/api.php/venta`
Registrar nueva venta

### GET `/api.php/status`
Estado del sistema

## 🔧 Troubleshooting

### Error: "API no responde"
- ✅ Verifica que `api.php` esté en el servidor
- ✅ Comprueba permisos de escritura
- ✅ Revisa logs de PHP

### Error: "CORS bloqueado"
- ✅ Asegúrate de que `.htaccess` esté presente
- ✅ En Nginx, aplica configuración del ejemplo

### Los datos no se guardan
- ✅ Verifica permisos de escritura en directorio
- ✅ Comprueba que PHP tenga permisos de archivo

## 📈 Características

- 🎯 **Detección automática** de entorno
- 🔄 **Sincronización en tiempo real**
- 📱 **Responsive design**
- 🛡️ **Protección por contraseña**
- 📊 **Estadísticas avanzadas**
- 💾 **Persistencia garantizada**
- 🌐 **Compatible con cualquier hosting**

## 📞 Soporte

Si tienes problemas:
1. Verifica la consola del navegador (F12)
2. Comprueba logs del servidor
3. Asegúrate de que todos los archivos estén subidos
4. Verifica permisos de PHP

¡El sistema está diseñado para funcionar sin configuración adicional!