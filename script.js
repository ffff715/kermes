// Configuración dinámica de API
const API_CONFIG = {
  // Detectar automáticamente si estamos en desarrollo local o servidor remoto
  getBaseURL: function() {
    const hostname = window.location.hostname;
    const isLocal = hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1';
    
    if (isLocal) {
      // Desarrollo local - usar servidor Python
      return 'http://127.0.0.1:5000';
    } else {
      // Servidor remoto - usar API PHP
      return window.location.origin;
    }
  },
  
  getAPIEndpoint: function(endpoint) {
    const baseURL = this.getBaseURL();
    const hostname = window.location.hostname;
    const isLocal = hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1';
    
    if (isLocal) {
      // Desarrollo local - endpoints Python
      return `${baseURL}/api/${endpoint}`;
    } else {
      // Servidor remoto - endpoints PHP
      return `${baseURL}/api.php/${endpoint}`;
    }
  }
};

// Para compatibilidad con código existente
const API_BASE = API_CONFIG.getBaseURL();

console.log('🌐 Configuración de API:', {
  hostname: window.location.hostname,
  isLocal: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1',
  baseURL: API_CONFIG.getBaseURL(),
  example: API_CONFIG.getAPIEndpoint('configuracion')
});

// Configuraciones de productos por categoría
const PRODUCTOS_POR_CATEGORIA = {
  frutas: {
    nombre: "Frutas Frescas",
    emoji: "🍎",
    productos: [
      {nombre: "Manzana", valor: 5.3},
      {nombre: "Banana", valor: 3},
      {nombre: "Naranja", valor: 4},
      {nombre: "Pera", valor: 2},
      {nombre: "Uva", valor: 6}
    ]
  },
  bebidas: {
    nombre: "Bebidas",
    emoji: "🥤",
    productos: [
      {nombre: "Coca Cola", valor: 2.5},
      {nombre: "Agua", valor: 1},
      {nombre: "Jugo Naranja", valor: 3.5},
      {nombre: "Red Bull", valor: 4},
      {nombre: "Cerveza", valor: 3}
    ]
  },
  snacks: {
    nombre: "Snacks",
    emoji: "🍿",
    productos: [
      {nombre: "Papitas", valor: 2},
      {nombre: "Chocolate", valor: 3.5},
      {nombre: "Galletas", valor: 2.5},
      {nombre: "Chicles", valor: 1},
      {nombre: "Caramelos", valor: 1.5}
    ]
  },
  panaderia: {
    nombre: "Panadería",
    emoji: "🥖",
    productos: [
      {nombre: "Pan", valor: 1.5},
      {nombre: "Croissant", valor: 3},
      {nombre: "Pastel", valor: 5},
      {nombre: "Donut", valor: 2.5},
      {nombre: "Muffin", valor: 3.5}
    ]
  }
};

// Lógica para opciones.html
if (window.location.pathname.endsWith('opciones.html')) {
  // Obtener categoría desde URL
  const urlParams = new URLSearchParams(window.location.search);
  const categoria = urlParams.get('categoria') || 'frutas';
  const configCategoria = PRODUCTOS_POR_CATEGORIA[categoria];
  
  if (!configCategoria) {
    alert('Categoría no válida, redirigiendo...');
    window.location.href = 'index.html';
  }
  
  // Actualizar título de la página
  document.title = `Ventas - ${configCategoria.nombre}`;
  
  // Cargar configuración y datos desde el servidor
  Promise.all([
    fetch(API_CONFIG.getAPIEndpoint('configuracion')).then(res => res.json()),
    fetch(API_CONFIG.getAPIEndpoint('datos')).then(res => res.json())
  ]).then(([configuracion, data]) => {
    const casillasDiv = document.getElementById('casillas');
    let totalCasillas = 0;
    let decisionSeleccionada = 10; // Por defecto la primera decisión
    let casillasSeleccionadas = [];
    const porcentajeExtra = configuracion.porcentajeBeneficio / 100; // Usar porcentaje del servidor
    
    console.log('📊 Configuración cargada desde servidor:', configuracion);
    console.log('🏷️ Categoría seleccionada:', categoria, configCategoria);
    
    // Agregar título de categoría
    const titulo = document.querySelector('h1');
    if (titulo) {
      titulo.textContent = `${configCategoria.emoji} Ventas - ${configCategoria.nombre}`;
    }
    
    // Agregar botón de volver
    const volverBtn = document.createElement('div');
    volverBtn.innerHTML = `
      <button onclick="window.location.href='index.html'" 
              style="background: #95a5a6; color: white; border: none; padding: 0.5em 1em; 
                     border-radius: 5px; cursor: pointer; margin-bottom: 1em;">
        ← Volver a Categorías
      </button>
    `;
    casillasDiv.parentNode.insertBefore(volverBtn, casillasDiv);
    
    function calcularYMostrarTotal() {
      document.getElementById('total').textContent = 'Total: ' + totalCasillas.toFixed(2) + ' €';
      
      const subtotal = totalCasillas + decisionSeleccionada;
      const extra = subtotal * porcentajeExtra;
      const resultadoFinal = subtotal + extra;
      
      document.getElementById('resultado').innerHTML = 
        '<h2>Total Final: ' + resultadoFinal.toFixed(2) + ' €</h2>';
    }
    
    function reiniciarTodo() {
      // Desmarcar todas las casillas
      document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        cb.checked = false;
      });
      
      // Resetear primera decisión como activa
      document.querySelectorAll('.decision').forEach(b => b.classList.remove('activo'));
        document.querySelector('.decision').classList.add('activo');
        
        // Resetear variables
        totalCasillas = 0;
        decisionSeleccionada = 10;
        casillasSeleccionadas = [];
        
        // Actualizar pantalla
        calcularYMostrarTotal();
        
        // Limpiar mensaje
        setTimeout(() => {
          document.getElementById('mensaje').innerHTML = '';
        }, 2000);
      }
      
      // Crear casillas usando productos de la categoría seleccionada
      configCategoria.productos.forEach((item, idx) => {
        const label = document.createElement('label');
        label.className = 'casilla';
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = item.valor;
        checkbox.dataset.nombre = item.nombre;
        checkbox.addEventListener('change', function() {
          if (this.checked) {
            totalCasillas += item.valor;
            casillasSeleccionadas.push({nombre: item.nombre, valor: item.valor});
          } else {
            totalCasillas -= item.valor;
            casillasSeleccionadas = casillasSeleccionadas.filter(c => c.nombre !== item.nombre);
          }
          calcularYMostrarTotal();
        });
        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(' ' + item.nombre + ' (' + item.valor + ' €)'));
        casillasDiv.appendChild(label);
      });
      
      // Manejar botones de decisión (solo uno activo)
      document.querySelectorAll('.decision').forEach(btn => {
        btn.addEventListener('click', function() {
          // Quitar clase activa de todos los botones
          document.querySelectorAll('.decision').forEach(b => b.classList.remove('activo'));
          // Añadir clase activa al botón clickeado
          this.classList.add('activo');
          // Guardar el valor de la decisión seleccionada
          decisionSeleccionada = parseFloat(this.dataset.valor);
          calcularYMostrarTotal();
        });
      });
      
      // Botón vender - Enviar al servidor Python
      document.getElementById('vender').addEventListener('click', async function() {
        const subtotal = totalCasillas + decisionSeleccionada;
        const extra = subtotal * porcentajeExtra;
        const resultadoFinal = subtotal + extra;
        
        // Crear objeto de venta
        const venta = {
          categoria: categoria,
          categoriaInfo: {
            nombre: configCategoria.nombre,
            emoji: configCategoria.emoji
          },
          casillas: [...casillasSeleccionadas],
          decision: {
            nombre: document.querySelector('.decision.activo').textContent,
            valor: decisionSeleccionada
          },
          totalCasillas: totalCasillas,
          subtotal: subtotal,
          extra: extra,
          total: resultadoFinal
        };
        
        try {
          // Enviar al servidor
          const response = await fetch(API_CONFIG.getAPIEndpoint('ventas'), {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(venta)
          });
          
          const resultado = await response.json();
          
          if (resultado.success) {
            // Mostrar mensaje de éxito
            document.getElementById('mensaje').innerHTML = 
              '<p style="color: green; font-weight: bold;">✅ Venta guardada en servidor: ' + resultadoFinal.toFixed(2) + ' €</p>';
            
            console.log('📊 Venta enviada al servidor:', venta);
          } else {
            throw new Error(resultado.error || 'Error desconocido');
          }
        } catch (error) {
          console.error('❌ Error al enviar venta:', error);
          document.getElementById('mensaje').innerHTML = 
            '<p style="color: red; font-weight: bold;">❌ Error al guardar venta. Verifique que el servidor esté activo.</p>';
        }
        
        // Reiniciar todo
        reiniciarTodo();
      });
      
      // Marcar el primer botón como activo por defecto
      document.querySelector('.decision').classList.add('activo');
      
      // Inicializar total
      calcularYMostrarTotal();
    });
}