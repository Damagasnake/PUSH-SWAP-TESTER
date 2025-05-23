#!/usr/bin/env python3
import subprocess
import sys
import random
import os
import webbrowser
import platform
import json

# Ruta al programa push_swap
PUSH_SWAP = "./push_swap"

# Colores para los elementos de las pilas (formato JavaScript)
COLORS = [
    "#FF5733", "#33FF57", "#3357FF", "#F033FF", "#FF33F0",
    "#FFC300", "#00FFC3", "#C300FF", "#FF0000", "#00FF00"
]

def generate_html(numbers, operations):
    """Genera un archivo HTML con la visualización interactiva de push_swap"""
    
    # Aseguramos que operations es una lista de strings y no está vacía
    if not operations:
        operations = []
    
    # Convertir a JSON para pasar correctamente a JavaScript
    numbers_json = json.dumps(numbers)
    operations_json = json.dumps(operations)
    colors_json = json.dumps(COLORS)
    
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Push Swap Visualizer</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #1e1e1e;
                color: #f0f0f0;
                margin: 0;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            h1 {
                text-align: center;
                color: #66c2ff;
            }
            
            .controls {
                display: flex;
                justify-content: center;
                margin: 20px 0;
                gap: 10px;
            }
            
            button {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 10px 15px;
                cursor: pointer;
                border-radius: 4px;
                font-size: 16px;
            }
            
            button:hover {
                background-color: #66c2ff;
            }
            
            .info {
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
            }
            
            .stacks-container {
                display: flex;
                justify-content: space-around;
                margin-top: 20px;
                min-height: 500px;
            }
            
            .stack {
                width: 45%;
                background-color: #2a2a2a;
                border-radius: 8px;
                padding: 15px;
                position: relative;
                min-height: 500px;
            }
            
            .stack-title {
                text-align: center;
                font-size: 24px;
                margin-bottom: 15px;
                color: #66c2ff;
            }
            
            .stack-items {
                display: flex;
                flex-direction: column-reverse;
                align-items: center;
                height: 500px;
                overflow-y: auto;
                gap: 5px;
            }
            
            .stack-item {
                width: 90%;
                background-color: #3a3a3a;
                color: white;
                text-align: center;
                border-radius: 4px;
                padding: 10px 0;
                transition: all 0.3s ease;
                position: relative;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            
            .operations {
                background-color: #2a2a2a;
                border-radius: 8px;
                padding: 15px;
                margin-top: 20px;
                height: 100px;
                overflow-y: auto;
            }
            
            .operation {
                padding: 5px;
                margin: 5px 0;
                border-radius: 4px;
            }
            
            .current-operation {
                background-color: #66c2ff;
                color: #1e1e1e;
                font-weight: bold;
            }
            
            .speed-control {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-top: 10px;
                justify-content: center;
            }
            
            .speed-slider {
                width: 200px;
            }
            
            .debug-info {
                margin-top: 20px;
                padding: 10px;
                background-color: #333;
                border-radius: 4px;
                font-family: monospace;
                white-space: pre-wrap;
            }

            /* Estilo para mostrar las pilas más claramente */
            .empty-stack-message {
                text-align: center;
                color: #666;
                padding: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Push Swap Visualizer</h1>
            
            <div class="controls">
                <button id="start">▶ Empezar</button>
                <button id="step">➡ Paso a paso</button>
                <button id="reset">🔄 Reiniciar</button>
            </div>
            
            <div class="speed-control">
                <label for="speed">Velocidad:</label>
                <input type="range" id="speed" class="speed-slider" min="50" max="1000" value="300">
                <span id="speed-value">300ms</span>
            </div>
            
            <div class="info">
                <div id="total-operations">Operaciones totales: <span>0</span></div>
                <div id="current-step">Paso actual: <span>0</span> / <span>0</span></div>
            </div>
            
            <div class="stacks-container">
                <div class="stack">
                    <div class="stack-title">Pila A</div>
                    <div class="stack-items" id="stack-a"></div>
                </div>
                
                <div class="stack">
                    <div class="stack-title">Pila B</div>
                    <div class="stack-items" id="stack-b"></div>
                </div>
            </div>
            
            <div class="operations" id="operations-list">
                <div class="operation">Esperando inicio...</div>
            </div>
            
            <div class="debug-info">
                <h3>Información de depuración</h3>
                <p>Números iniciales: """ + str(numbers) + """</p>
                <p>Total de operaciones: """ + str(len(operations)) + """</p>
                <p>Operaciones: """ + str(operations) + """</p>
            </div>
        </div>
        
        <script>
            // Estado inicial de las pilas (usando JSON para transferir datos de Python a JavaScript)
            const initialNumbers = """ + numbers_json + """;
            const operations = """ + operations_json + """;
            const COLORS = """ + colors_json + """;
            
            console.log("Números iniciales:", initialNumbers);
            console.log("Operaciones:", operations);
            console.log("Colores:", COLORS);
            
            let stackA = [...initialNumbers];
            let stackB = [];
            let currentStep = 0;
            let animationInterval = null;
            let animationSpeed = 300; // milisegundos
            
            // Obtener el elemento máximo para calcular proporciones
            const maxNum = Math.max(...initialNumbers);
            const minNum = Math.min(...initialNumbers);
            const range = maxNum - minNum;
            
            // Elementos del DOM
            const stackAElement = document.getElementById('stack-a');
            const stackBElement = document.getElementById('stack-b');
            const operationsList = document.getElementById('operations-list');
            const totalOpsElement = document.getElementById('total-operations').querySelector('span');
            const currentStepElements = document.getElementById('current-step').querySelectorAll('span');
            const startButton = document.getElementById('start');
            const stepButton = document.getElementById('step');
            const resetButton = document.getElementById('reset');
            const speedSlider = document.getElementById('speed');
            const speedValue = document.getElementById('speed-value');
            
            // Inicializar visualización
            function init() {
                stackA = [...initialNumbers];
                stackB = [];
                currentStep = 0;
                
                renderStacks();
                renderOperations();
                
                totalOpsElement.textContent = operations.length;
                currentStepElements[0].textContent = 0;
                currentStepElements[1].textContent = operations.length;
                
                if (animationInterval) {
                    clearInterval(animationInterval);
                    animationInterval = null;
                }
            }
            
            // Renderizar las pilas
            function renderStacks() {
                console.log("Renderizando pilas");
                console.log("stackA:", stackA);
                console.log("stackB:", stackB);
                
                // Limpiar pilas
                stackAElement.innerHTML = '';
                stackBElement.innerHTML = '';
                
                // Renderizar pila A
                if (stackA.length === 0) {
                    const emptyMessage = document.createElement('div');
                    emptyMessage.classList.add('empty-stack-message');
                    emptyMessage.textContent = "Pila A vacía";
                    stackAElement.appendChild(emptyMessage);
                } else {
                    stackA.forEach((num, index) => {
                        const item = document.createElement('div');
                        item.classList.add('stack-item');
                        
                        // Calcular ancho proporcional al valor
                        const widthPercent = range === 0 ? 90 : 30 + ((num - minNum) / range) * 60;
                        item.style.width = `${widthPercent}%`;
                        
                        // Asignar un color basado en el valor
                        const colorIndex = Math.abs(num) % COLORS.length;
                        item.style.backgroundColor = COLORS[colorIndex];
                        
                        item.textContent = num;
                        stackAElement.appendChild(item);
                    });
                }
                
                // Renderizar pila B
                if (stackB.length === 0) {
                    const emptyMessage = document.createElement('div');
                    emptyMessage.classList.add('empty-stack-message');
                    emptyMessage.textContent = "Pila B vacía";
                    stackBElement.appendChild(emptyMessage);
                } else {
                    stackB.forEach((num, index) => {
                        const item = document.createElement('div');
                        item.classList.add('stack-item');
                        
                        // Calcular ancho proporcional al valor
                        const widthPercent = range === 0 ? 90 : 30 + ((num - minNum) / range) * 60;
                        item.style.width = `${widthPercent}%`;
                        
                        // Asignar un color basado en el valor
                        const colorIndex = Math.abs(num) % COLORS.length;
                        item.style.backgroundColor = COLORS[colorIndex];
                        
                        item.textContent = num;
                        stackBElement.appendChild(item);
                    });
                }
            }
            
            // Renderizar lista de operaciones
            function renderOperations() {
                operationsList.innerHTML = '';
                
                if (operations.length === 0) {
                    const opElement = document.createElement('div');
                    opElement.classList.add('operation');
                    opElement.textContent = "No hay operaciones (lista ya ordenada o error)";
                    operationsList.appendChild(opElement);
                    return;
                }
                
                operations.forEach((op, index) => {
                    const opElement = document.createElement('div');
                    opElement.classList.add('operation');
                    if (index === currentStep - 1) {
                        opElement.classList.add('current-operation');
                    }
                    opElement.textContent = `${index + 1}: ${op}`;
                    operationsList.appendChild(opElement);
                });
                
                // Scrollear a la operación actual
                if (currentStep > 0) {
                    const currentOpElement = operationsList.querySelector('.current-operation');
                    if (currentOpElement) {
                        currentOpElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            }
            
            // Ejecutar una operación
            function executeOperation(op) {
                console.log("Ejecutando operación:", op);
                switch(op) {
                    case 'sa':
                        // Swap A - intercambiar los dos primeros elementos de A
                        if (stackA.length >= 2) {
                            const temp = stackA[0];
                            stackA[0] = stackA[1];
                            stackA[1] = temp;
                        }
                        break;
                    case 'sb':
                        // Swap B - intercambiar los dos primeros elementos de B
                        if (stackB.length >= 2) {
                            const temp = stackB[0];
                            stackB[0] = stackB[1];
                            stackB[1] = temp;
                        }
                        break;
                    case 'ss':
                        // Swap A y Swap B simultáneamente
                        if (stackA.length >= 2) {
                            const temp = stackA[0];
                            stackA[0] = stackA[1];
                            stackA[1] = temp;
                        }
                        if (stackB.length >= 2) {
                            const temp = stackB[0];
                            stackB[0] = stackB[1];
                            stackB[1] = temp;
                        }
                        break;
                    case 'pa':
                        // Push A - tomar el primer elemento de B y ponerlo en A
                        if (stackB.length > 0) {
                            const elem = stackB.shift();
                            stackA.unshift(elem);
                        }
                        break;
                    case 'pb':
                        // Push B - tomar el primer elemento de A y ponerlo en B
                        if (stackA.length > 0) {
                            const elem = stackA.shift();
                            stackB.unshift(elem);
                        }
                        break;
                    case 'ra':
                        // Rotate A - mover el primer elemento al final de A
                        if (stackA.length > 0) {
                            const elem = stackA.shift();
                            stackA.push(elem);
                        }
                        break;
                    case 'rb':
                        // Rotate B - mover el primer elemento al final de B
                        if (stackB.length > 0) {
                            const elem = stackB.shift();
                            stackB.push(elem);
                        }
                        break;
                    case 'rr':
                        // Rotate A y Rotate B simultáneamente
                        if (stackA.length > 0) {
                            const elemA = stackA.shift();
                            stackA.push(elemA);
                        }
                        if (stackB.length > 0) {
                            const elemB = stackB.shift();
                            stackB.push(elemB);
                        }
                        break;
                    case 'rra':
                        // Reverse Rotate A - mover el último elemento al inicio de A
                        if (stackA.length > 0) {
                            const elem = stackA.pop();
                            stackA.unshift(elem);
                        }
                        break;
                    case 'rrb':
                        // Reverse Rotate B - mover el último elemento al inicio de B
                        if (stackB.length > 0) {
                            const elem = stackB.pop();
                            stackB.unshift(elem);
                        }
                        break;
                    case 'rrr':
                        // Reverse Rotate A y Reverse Rotate B simultáneamente
                        if (stackA.length > 0) {
                            const elemA = stackA.pop();
                            stackA.unshift(elemA);
                        }
                        if (stackB.length > 0) {
                            const elemB = stackB.pop();
                            stackB.unshift(elemB);
                        }
                        break;
                    default:
                        console.error("Operación desconocida:", op);
                        break;
                }
                console.log("Estado de pila A después de operación:", stackA);
                console.log("Estado de pila B después de operación:", stackB);
            }
            
            // Ejecutar un paso
            function step() {
                if (currentStep < operations.length) {
                    executeOperation(operations[currentStep]);
                    currentStep++;
                    
                    renderStacks();
                    renderOperations();
                    
                    currentStepElements[0].textContent = currentStep;
                    
                    return true;
                }
                return false;
            }
            
            // Empezar animación automática
            function start() {
                if (animationInterval) {
                    clearInterval(animationInterval);
                    startButton.textContent = '▶ Empezar';
                    animationInterval = null;
                    return;
                }
                
                if (currentStep >= operations.length) {
                    init();
                }
                
                startButton.textContent = '⏸ Pausar';
                
                animationInterval = setInterval(() => {
                    if (!step()) {
                        clearInterval(animationInterval);
                        animationInterval = null;
                        startButton.textContent = '▶ Empezar';
                    }
                }, animationSpeed);
            }
            
            // Reiniciar visualización
            function reset() {
                init();
            }
            
            // Event listeners
            startButton.addEventListener('click', start);
            stepButton.addEventListener('click', step);
            resetButton.addEventListener('click', reset);
            
            // Control de velocidad
            speedSlider.addEventListener('input', function() {
                animationSpeed = parseInt(this.value);
                speedValue.textContent = `${animationSpeed}ms`;
                
                if (animationInterval) {
                    clearInterval(animationInterval);
                    animationInterval = setInterval(() => {
                        if (!step()) {
                            clearInterval(animationInterval);
                            animationInterval = null;
                            startButton.textContent = '▶ Empezar';
                        }
                    }, animationSpeed);
                }
            });
            
            // Inicializar visualización al cargar el documento
            document.addEventListener('DOMContentLoaded', () => {
                console.log("DOM cargado, inicializando visualización");
                init();
            });
            
            // Inicializar inmediatamente también 
            init();
        </script>
    </body>
    </html>
    """
    
    # Guardar el HTML en un archivo
    with open("push_swap_visualization.html", "w") as f:
        f.write(html)
    
    return "push_swap_visualization.html"

def run_push_swap(numbers):
    """Ejecuta push_swap con los números dados y devuelve las operaciones"""
    try:
        # Convertir números a strings
        num_strings = [str(n) for n in numbers]
        
        # Mostrar el comando que se va a ejecutar
        cmd = [PUSH_SWAP] + num_strings
        print(f"Ejecutando comando: {' '.join(cmd)}")
        
        # Ejecutar push_swap
        result = subprocess.run(cmd, 
                                 capture_output=True, 
                                 text=True)
        
        # Mostrar salida completa para debug
        print(f"Código de salida: {result.returncode}")
        print(f"Stdout: '{result.stdout}'")
        print(f"Stderr: '{result.stderr}'")
        
        # Comprobar si hubo algún error
        if result.returncode != 0:
            print(f"Error ejecutando push_swap: {result.stderr}")
            return []
        
        # Obtener las operaciones devueltas
        operations = result.stdout.strip().split('\n')
        # Filtrar líneas vacías
        operations = [op for op in operations if op]
        
        print(f"Operaciones obtenidas: {operations}")
        return operations
    except Exception as e:
        print(f"Error al ejecutar push_swap: {e}")
        import traceback
        traceback.print_exc()
        return []

def generate_random_numbers(count=10, min_val=-100, max_val=100):
    """Genera una lista de números aleatorios sin repetición"""
    numbers = random.sample(range(min_val, max_val + 1), min(count, max_val - min_val + 1))
    return numbers

def open_in_browser(filepath):
    """Abre el archivo HTML en el navegador predeterminado"""
    # Obtener URL completa
    url = "file://" + os.path.abspath(filepath)
    print(f"Abriendo URL: {url}")
    
    # Abrir navegador
    webbrowser.open(url)

def main():
    try:
        numbers = []
        
        # Comprobar si se proporcionaron argumentos
        if len(sys.argv) > 1:
            # Si hay argumentos, intentar convertirlos a enteros
            try:
                numbers = [int(arg) for arg in sys.argv[1:]]
            except ValueError:
                print("Error: Todos los argumentos deben ser números enteros.")
                sys.exit(1)
        else:
            # Si no hay argumentos, generar 10 números aleatorios
            numbers = generate_random_numbers(10)
        
        # Verificar que no hay duplicados
        if len(numbers) != len(set(numbers)):
            print("Error: No se permiten números duplicados.")
            sys.exit(1)
        
        print(f"Números a ordenar: {numbers}")
        
        # Ejecutar push_swap
        operations = run_push_swap(numbers)
        
        # Generar visualización incluso si no hay operaciones
        print(f"Generando visualización con {len(operations)} operaciones")
        html_file = generate_html(numbers, operations)
        
        # Abrir en navegador
        print(f"Abriendo visualización en el navegador...")
        open_in_browser(html_file)
            
    except Exception as e:
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()