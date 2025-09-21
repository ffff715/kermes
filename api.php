<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Manejar preflight requests
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Archivos de datos
$configFile = 'configuracion.json';
$datosFile = 'datos.json';

// Función para leer archivo JSON
function leerJSON($archivo) {
    if (!file_exists($archivo)) {
        return null;
    }
    $contenido = file_get_contents($archivo);
    return json_decode($contenido, true);
}

// Función para escribir archivo JSON
function escribirJSON($archivo, $datos) {
    $json = json_encode($datos, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    return file_put_contents($archivo, $json, LOCK_EX) !== false;
}

// Crear archivos por defecto si no existen
function crearArchivosDefecto() {
    global $configFile, $datosFile;
    
    // Configuración por defecto
    if (!file_exists($configFile)) {
        $configDefecto = [
            'porcentajeBeneficio' => 15,
            'costes' => [
                'Manzana' => 2.5,
                'Banana' => 1.5,
                'Naranja' => 2.0,
                'Pera' => 1.0,
                'Uva' => 3.0
            ],
            'costeDecisiones' => [
                'Decisión A' => 5,
                'Decisión B' => 10,
                'Decisión C' => 15,
                'Decisión D' => 20
            ]
        ];
        escribirJSON($configFile, $configDefecto);
    }
    
    // Datos por defecto
    if (!file_exists($datosFile)) {
        $datosDefecto = [
            'ventas' => [],
            'casillas' => [
                ['nombre' => 'Manzana', 'valor' => 5.3],
                ['nombre' => 'Banana', 'valor' => 3],
                ['nombre' => 'Naranja', 'valor' => 4],
                ['nombre' => 'Pera', 'valor' => 2],
                ['nombre' => 'Uva', 'valor' => 6]
            ]
        ];
        escribirJSON($datosFile, $datosDefecto);
    }
}

// Crear archivos si no existen
crearArchivosDefecto();

// Obtener método y ruta
$metodo = $_SERVER['REQUEST_METHOD'];
$ruta = $_SERVER['REQUEST_URI'];
$rutaLimpia = parse_url($ruta, PHP_URL_PATH);
$rutaParts = explode('/', trim($rutaLimpia, '/'));

// Encontrar 'api.php' en la ruta y obtener lo que sigue
$apiIndex = array_search('api.php', $rutaParts);
if ($apiIndex !== false && isset($rutaParts[$apiIndex + 1])) {
    $endpoint = $rutaParts[$apiIndex + 1];
} else {
    // Si no hay endpoint específico, usar query parameter
    $endpoint = isset($_GET['endpoint']) ? $_GET['endpoint'] : '';
}

try {
    switch ($endpoint) {
        case 'configuracion':
            if ($metodo === 'GET') {
                // Obtener configuración
                $config = leerJSON($configFile);
                if ($config === null) {
                    http_response_code(404);
                    echo json_encode(['error' => 'Configuración no encontrada']);
                } else {
                    echo json_encode($config);
                }
            } elseif ($metodo === 'POST') {
                // Actualizar configuración
                $input = json_decode(file_get_contents('php://input'), true);
                if ($input === null) {
                    http_response_code(400);
                    echo json_encode(['error' => 'JSON inválido']);
                } else {
                    if (escribirJSON($configFile, $input)) {
                        echo json_encode(['success' => true, 'message' => 'Configuración actualizada']);
                    } else {
                        http_response_code(500);
                        echo json_encode(['error' => 'Error al guardar configuración']);
                    }
                }
            }
            break;
            
        case 'datos':
            if ($metodo === 'GET') {
                // Obtener datos
                $datos = leerJSON($datosFile);
                if ($datos === null) {
                    http_response_code(404);
                    echo json_encode(['error' => 'Datos no encontrados']);
                } else {
                    echo json_encode($datos);
                }
            } elseif ($metodo === 'POST') {
                // Actualizar datos completos
                $input = json_decode(file_get_contents('php://input'), true);
                if ($input === null) {
                    http_response_code(400);
                    echo json_encode(['error' => 'JSON inválido']);
                } else {
                    if (escribirJSON($datosFile, $input)) {
                        echo json_encode(['success' => true, 'message' => 'Datos actualizados']);
                    } else {
                        http_response_code(500);
                        echo json_encode(['error' => 'Error al guardar datos']);
                    }
                }
            }
            break;
            
        case 'ventas':
            if ($metodo === 'GET') {
                // Obtener datos
                $datos = leerJSON($datosFile);
                if ($datos === null) {
                    http_response_code(404);
                    echo json_encode(['error' => 'Datos no encontrados']);
                } else {
                    echo json_encode($datos);
                }
            } elseif ($metodo === 'POST') {
                // Agregar nueva venta
                $input = json_decode(file_get_contents('php://input'), true);
                if ($input === null) {
                    http_response_code(400);
                    echo json_encode(['error' => 'JSON inválido']);
                } else {
                    $datos = leerJSON($datosFile);
                    if ($datos === null) {
                        $datos = ['ventas' => [], 'casillas' => []];
                    }
                    
                    // Agregar timestamp si no existe
                    if (!isset($input['fecha'])) {
                        $input['fecha'] = date('Y-m-d H:i:s');
                    }
                    
                    $datos['ventas'][] = $input;
                    
                    if (escribirJSON($datosFile, $datos)) {
                        echo json_encode(['success' => true, 'message' => 'Venta registrada']);
                    } else {
                        http_response_code(500);
                        echo json_encode(['error' => 'Error al guardar venta']);
                    }
                }
            } elseif ($metodo === 'DELETE') {
                // Borrar todas las ventas
                $datos = leerJSON($datosFile);
                if ($datos === null) {
                    $datos = ['ventas' => [], 'casillas' => []];
                } else {
                    $datos['ventas'] = []; // Vaciar solo el array de ventas
                }
                
                if (escribirJSON($datosFile, $datos)) {
                    echo json_encode(['success' => true, 'message' => 'Todas las ventas borradas']);
                } else {
                    http_response_code(500);
                    echo json_encode(['error' => 'Error al borrar ventas']);
                }
            }
            break;
            
        case 'reset':
            if ($metodo === 'POST') {
                // Resetear datos
                $datosLimpios = [
                    'ventas' => [],
                    'casillas' => [
                        ['nombre' => 'Manzana', 'valor' => 5.3],
                        ['nombre' => 'Banana', 'valor' => 3],
                        ['nombre' => 'Naranja', 'valor' => 4],
                        ['nombre' => 'Pera', 'valor' => 2],
                        ['nombre' => 'Uva', 'valor' => 6]
                    ]
                ];
                
                if (escribirJSON($datosFile, $datosLimpios)) {
                    echo json_encode(['success' => true, 'message' => 'Datos reseteados']);
                } else {
                    http_response_code(500);
                    echo json_encode(['error' => 'Error al resetear datos']);
                }
            }
            break;
            
        case 'status':
            // Estado del sistema
            echo json_encode([
                'status' => 'online',
                'timestamp' => date('Y-m-d H:i:s'),
                'files' => [
                    'configuracion' => file_exists($configFile),
                    'datos' => file_exists($datosFile)
                ]
            ]);
            break;
            
        default:
            http_response_code(404);
            echo json_encode([
                'error' => 'Endpoint no encontrado',
                'available_endpoints' => [
                    'GET api.php/configuracion - Obtener configuración',
                    'POST api.php/configuracion - Actualizar configuración',
                    'GET api.php/datos - Obtener datos',
                    'POST api.php/datos - Actualizar datos',
                    'POST api.php/ventas - Agregar venta',
                    'POST api.php/reset - Resetear datos',
                    'GET api.php/status - Estado del sistema'
                ]
            ]);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Error interno: ' . $e->getMessage()]);
}
?>