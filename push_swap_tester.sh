#!/bin/bash

# Colores para mejorar la visualización
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Path al programa push_swap (ajusta según sea necesario)
PUSH_SWAP="./push_swap"

# Función para mostrar el encabezado de una prueba
print_header() {
    echo -e "\n${BLUE}=======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=======================================${NC}"
}

# Función para verificar si el programa detecta errores correctamente
test_error_cases() {
    print_header "PRUEBA DE CASOS DE ERROR"

    echo -e "${YELLOW}Caso: Argumentos duplicados${NC}"
    OUTPUT=$($PUSH_SWAP 1 2 3 3 4 5 2>&1)
    if [[ "$OUTPUT" == *"Error"* ]]; then
        echo -e "${GREEN}✓ Correcto: Detectó duplicados${NC}"
    else
        echo -e "${RED}✗ Incorrecto: No detectó duplicados${NC}"
    fi

    echo -e "${YELLOW}Caso: Argumentos no numéricos${NC}"
    OUTPUT=$($PUSH_SWAP 1 2 abc 4 5 2>&1)
    if [[ "$OUTPUT" == *"Error"* ]]; then
        echo -e "${GREEN}✓ Correcto: Detectó argumento no numérico${NC}"
    else
        echo -e "${RED}✗ Incorrecto: No detectó argumento no numérico${NC}"
    fi

    echo -e "${YELLOW}Caso: Número fuera de rango INT${NC}"
    OUTPUT=$($PUSH_SWAP 1 2 99999999999999999999 4 2>&1)
    if [[ "$OUTPUT" == *"Error"* ]]; then
        echo -e "${GREEN}✓ Correcto: Detectó número fuera de rango${NC}"
    else
        echo -e "${RED}✗ Incorrecto: No detectó número fuera de rango${NC}"
    fi
}

# Función para probar casos básicos
test_basic_cases() {
    print_header "PRUEBA DE CASOS BÁSICOS"

    echo -e "${YELLOW}Caso: Lista ya ordenada${NC}"
    OPERATIONS=$($PUSH_SWAP 1 2 3 4 5 | wc -l | tr -d '[:space:]')
    echo -e "Operaciones: $OPERATIONS"
    if [[ "$OPERATIONS" -eq 0 ]]; then
        echo -e "${GREEN}✓ Correcto: No realizó operaciones en lista ordenada${NC}"
    else
        echo -e "${RED}✗ Incorrecto: Realizó operaciones innecesarias${NC}"
    fi

    echo -e "${YELLOW}Caso: Un solo número${NC}"
    OPERATIONS=$($PUSH_SWAP 42 | wc -l | tr -d '[:space:]')
    echo -e "Operaciones: $OPERATIONS"
    if [[ "$OPERATIONS" -eq 0 ]]; then
        echo -e "${GREEN}✓ Correcto: No realizó operaciones con un solo número${NC}"
    else
        echo -e "${RED}✗ Incorrecto: Realizó operaciones innecesarias${NC}"
    fi

    echo -e "${YELLOW}Caso: Dos números invertidos${NC}"
    OPERATIONS=$($PUSH_SWAP 2 1 | wc -l | tr -d '[:space:]')
    echo -e "Operaciones: $OPERATIONS"
    if [[ "$OPERATIONS" -le 1 ]]; then
        echo -e "${GREEN}✓ Correcto: Usó una operación o menos${NC}"
    else
        echo -e "${RED}✗ Incorrecto: Usó más de una operación${NC}"
    fi

    echo -e "${YELLOW}Caso: Tres números (3 1 2)${NC}"
    OPERATIONS=$($PUSH_SWAP 3 1 2 | wc -l | tr -d '[:space:]')
    echo -e "Operaciones: $OPERATIONS"
    if [[ "$OPERATIONS" -le 2 ]]; then
        echo -e "${GREEN}✓ Correcto: Usó dos operaciones o menos${NC}"
    else
        echo -e "${RED}✗ Incorrecto: Usó más de dos operaciones${NC}"
    fi
}

# Función para probar casos extremos
test_extreme_cases() {
    print_header "PRUEBA DE CASOS EXTREMOS"

    echo -e "${YELLOW}Caso: Valores INT_MIN e INT_MAX${NC}"
    OPERATIONS=$($PUSH_SWAP 2147483647 -2147483648 0 42 | wc -l | tr -d '[:space:]')
    echo -e "Operaciones: $OPERATIONS"
    if [[ "$OPERATIONS" -lt 20 ]]; then
        echo -e "${GREEN}✓ Bueno: Usó menos de 20 operaciones${NC}"
    else
        echo -e "${YELLOW}⚠ Regular: Usó más de 20 operaciones${NC}"
    fi

    echo -e "${YELLOW}Caso: Secuencia invertida (5 números)${NC}"
    OPERATIONS=$($PUSH_SWAP 5 4 3 2 1 | wc -l | tr -d '[:space:]')
    echo -e "Operaciones: $OPERATIONS"
    if [[ "$OPERATIONS" -lt 12 ]]; then
        echo -e "${GREEN}✓ Excelente: Usó menos de 12 operaciones${NC}"
    else
        echo -e "${YELLOW}⚠ Regular: Usó más de 12 operaciones${NC}"
    fi
}

# Función para probar sets de datos medianos y grandes
test_large_sets() {
    print_header "PRUEBA DE CONJUNTOS GRANDES"

    echo -e "${YELLOW}Caso: 100 números aleatorios${NC}"
    ARG=$(ruby -e "puts (1..100).to_a.shuffle.join(' ')")
    OPERATIONS=$($PUSH_SWAP $ARG | wc -l | tr -d '[:space:]')
    echo -e "Operaciones: $OPERATIONS"
    if [[ "$OPERATIONS" -lt 1500 ]]; then
        echo -e "${GREEN}✓ Excelente: Menos de 1500 operaciones${NC}"
    elif [[ "$OPERATIONS" -lt 5000 ]]; then
        echo -e "${YELLOW}⚠ Aceptable: Entre 1500 y 5000 operaciones${NC}"
    else
        echo -e "${RED}✗ Pobre: Más de 5000 operaciones${NC}"
    fi
    
    echo -e "${YELLOW}Caso: 500 números aleatorios${NC}"
    ARG=$(ruby -e "puts (1..500).to_a.shuffle.join(' ')")
    time_start=$(date +%s.%N)
    OPERATIONS=$($PUSH_SWAP $ARG | wc -l | tr -d '[:space:]')
    time_end=$(date +%s.%N)
    execution_time=$(echo "$time_end - $time_start" | bc)
    echo -e "Operaciones: $OPERATIONS (Tiempo: $execution_time segundos)"
    if [[ "$OPERATIONS" -lt 10000 ]]; then
        echo -e "${GREEN}✓ Excelente: Menos de 10000 operaciones${NC}"
    elif [[ "$OPERATIONS" -lt 30000 ]]; then
        echo -e "${YELLOW}⚠ Aceptable: Entre 10000 y 30000 operaciones${NC}"
    else
        echo -e "${RED}✗ Pobre: Más de 30000 operaciones${NC}"
    fi
}

# Función para probar la validez de las operaciones (requiere checker)
test_validity() {
    # Comprueba si existe un checker en el directorio
    if [ -f "./checker_Mac" ]; then
        CHECKER="./checker_Mac"
    elif [ -f "./checker" ]; then
        CHECKER="./checker"
    else
        echo -e "${RED}No se encontró el programa checker. Saltando prueba de validez.${NC}"
        return
    fi

    print_header "PRUEBA DE VALIDEZ DE OPERACIONES"

    echo -e "${YELLOW}Caso: 5 números aleatorios${NC}"
    ARG="3 1 4 2 5"
    OPERATIONS=$($PUSH_SWAP $ARG)
    echo "$OPERATIONS" | $CHECKER $ARG > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Correcto: La secuencia ordena correctamente${NC}"
    else
        echo -e "${RED}✗ Incorrecto: La secuencia no ordena correctamente${NC}"
    fi
    
    echo -e "${YELLOW}Caso: 100 números aleatorios${NC}"
    ARG=$(ruby -e "puts (1..100).to_a.shuffle.join(' ')")
    OPERATIONS=$($PUSH_SWAP $ARG)
    echo "$OPERATIONS" | $CHECKER $ARG > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Correcto: La secuencia ordena correctamente${NC}"
    else
        echo -e "${RED}✗ Incorrecto: La secuencia no ordena correctamente${NC}"
    fi
}

# Funcion para mostrar un resumen visual del rendimiento
show_performance_summary() {
    print_header "RESUMEN DE RENDIMIENTO"
    
    # Pruebas con diferentes tamaños para mostrar gráficamente
    sizes=(3 5 10 50 100 500)
    
    echo -e "${YELLOW}Tamaño\t| Operaciones\t| Gráfico${NC}"
    echo "------------------------------------"
    
    for size in "${sizes[@]}"; do
        ARG=$(ruby -e "puts (1..$size).to_a.shuffle.join(' ')")
        OPERATIONS=$($PUSH_SWAP $ARG | wc -l | tr -d '[:space:]')
        
        # Crear una barra gráfica sencilla
        bar=""
        bar_length=$((OPERATIONS / 20))
        if [ $bar_length -gt 50 ]; then
            bar_length=50
        fi
        
        for ((i=0; i<$bar_length; i++)); do
            bar="${bar}█"
        done
        
        echo -e "$size\t| $OPERATIONS\t| ${BLUE}$bar${NC}"
    done
}

# Ejecutar todas las pruebas
main() {
    print_header "TESTER DE PUSH_SWAP"
    echo -e "${YELLOW}Verificando existencia del programa push_swap...${NC}"
    
    # Verificar que el programa existe
    if [ ! -f "$PUSH_SWAP" ]; then
        echo -e "${RED}Error: No se encontró el programa push_swap en la ubicación: $PUSH_SWAP${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Programa encontrado. Ejecutando pruebas...${NC}"
    
    # Ejecutar todas las pruebas
    test_error_cases
    test_basic_cases
    test_extreme_cases
    test_large_sets
    test_validity
    show_performance_summary
    
    print_header "PRUEBAS COMPLETADAS"
}

# Ejecutar programa principal
main