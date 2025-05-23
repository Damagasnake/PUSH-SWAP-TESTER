# PUSH-SWAP-TESTER

A comprehensive testing suite for the 42 Push_swap project, featuring both a shell script tester and an interactive visualizer.

## 🧪 Shell Script Tester (`push_swap_tester.sh`)

The shell script tester provides extensive testing capabilities for your push_swap program, including:

### Features
- Error case detection (duplicates, non-numeric arguments, INT overflow)
- Basic case validation (sorted lists, single numbers, simple swaps)
- Extreme case testing (INT_MIN/MAX values, reversed sequences)
- Performance testing with various dataset sizes (100, 500 numbers)
- Operation count validation
- Visual performance summary
- Validity checking with the official checker

### Usage
```bash
# Make the tester executable
chmod +x push_swap_tester.sh

# Run the tester
./push_swap_tester.sh
```

### Test Categories
1. **Error Cases**: Tests how your program handles invalid inputs
2. **Basic Cases**: Verifies fundamental operations
3. **Extreme Cases**: Checks edge cases and boundary values
4. **Large Sets**: Tests performance with bigger datasets
5. **Validity**: Ensures all operations are valid (requires checker program)

## 🎮 Interactive Visualizer (`push_swap_visualizer.py`)

A dynamic, web-based visualizer that helps you understand how your push_swap algorithm works step by step.

### Features
- Real-time visualization of stack operations
- Interactive controls (Start, Step-by-step, Reset)
- Adjustable animation speed
- Operation count tracking
- Color-coded stack elements
- Debug information panel

### Requirements
- Python 3.x
- A modern web browser
- Your push_swap executable in the same directory

### Usage
```bash
# Make the visualizer executable
chmod +x push_swap_visualizer.py

# Run with random numbers (default: 10 numbers)
./push_swap_visualizer.py

# Run with specific number of random values
./push_swap_visualizer.py 15

# Run with custom values
./push_swap_visualizer.py 5 2 9 1 3
```

### Visualization Controls
- ▶ **Start**: Begins the automatic visualization
- ➡ **Step**: Move through operations one at a time
- 🔄 **Reset**: Return to initial state
- **Speed Slider**: Adjust animation speed

## 📋 Requirements

- Your push_swap executable should be in the same directory as the testers
- For the shell script tester, Ruby is required for random number generation
- For the visualizer, Python 3.x and a modern web browser are needed
- Optional: checker_Mac or checker executable for validity testing

## 🚀 Getting Started

1. Clone this repository into your push_swap project directory
2. Copy your push_swap executable to this directory
3. Make both testers executable:
   ```bash
   chmod +x push_swap_tester.sh push_swap_visualizer.py
   ```
4. Run either tester as needed

## 📝 Notes

- The shell script tester expects your push_swap executable to be named `push_swap`
- The visualizer will automatically open your default web browser
- For best results, ensure your terminal supports color output for the shell tester
- The visualizer creates a temporary HTML file for the visualization

## ⚠️ Troubleshooting

If you encounter any issues:
1. Ensure your push_swap executable is in the correct location
2. Verify you have the required dependencies installed
3. Check file permissions
4. For the visualizer, ensure your browser allows local file access

## 🔥 XTREME TESTING

Use these commands to thoroughly test your push_swap with challenging cases. Copy and paste them directly into your terminal.

### 🎯 Basic Edge Cases
```bash
# Test with negative numbers only
ARG="$(ruby -e "puts (-50..-1).to_a.shuffle.join(' ')")"; ./push_swap $ARG | ./checker_Mac $ARG

# Test with positive numbers only
ARG="$(ruby -e "puts (1..50).to_a.shuffle.join(' ')")"; ./push_swap $ARG | ./checker_Mac $ARG

# Test with alternating positive/negative
ARG="$(ruby -e "puts (-25..25).to_a.shuffle.join(' ')")"; ./push_swap $ARG | ./checker_Mac $ARG

# Test with duplicates (should print Error)
./push_swap 1 2 3 3 4 5

# Test with non-numeric values (should print Error)
./push_swap 1 2 3 abc 4 5
```

### 💪 Performance Tests
```bash
# Test with 100 numbers and count operations
ARG="$(ruby -e "puts (1..100).to_a.shuffle.join(' ')")"; ./push_swap $ARG | wc -l

# Test with 500 numbers and count operations
ARG="$(ruby -e "puts (1..500).to_a.shuffle.join(' ')")"; ./push_swap $ARG | wc -l

# Test with 100 numbers and verify sorting
ARG="$(ruby -e "puts (1..100).to_a.shuffle.join(' ')")"; ./push_swap $ARG | ./checker_Mac $ARG

# Test with 500 numbers and verify sorting
ARG="$(ruby -e "puts (1..500).to_a.shuffle.join(' ')")"; ./push_swap $ARG | ./checker_Mac $ARG
```

### 🧪 Stress Testing
```bash
# Test 10 different random sets of 100 numbers
for i in {1..10}; do
    echo "\nTest $i:";
    ARG="$(ruby -e "puts (1..100).to_a.shuffle.join(' ')")";
    NUM=$(./push_swap $ARG | wc -l);
    RESULT=$(./push_swap $ARG | ./checker_Mac $ARG);
    echo "Operations: $NUM";
    echo "Result: $RESULT";
done

# Test with maximum INT values
ARG="2147483647 -2147483648 0 1 -1"; ./push_swap $ARG | ./checker_Mac $ARG

# Test with almost sorted arrays (one swap needed)
ARG="1 3 2 4 5"; ./push_swap $ARG | ./checker_Mac $ARG
```

### 🔄 Reverse Order Tests
```bash
# Test with reverse ordered sets of different sizes
# 5 numbers
ARG="$(ruby -e "puts (1..5).to_a.reverse.join(' ')")"; ./push_swap $ARG | wc -l

# 10 numbers
ARG="$(ruby -e "puts (1..10).to_a.reverse.join(' ')")"; ./push_swap $ARG | wc -l

# 100 numbers
ARG="$(ruby -e "puts (1..100).to_a.reverse.join(' ')")"; ./push_swap $ARG | wc -l
```

### 🎲 Random Size Tests
```bash
# Test with random size between 1-500 numbers
SIZE=$((RANDOM % 500 + 1));
ARG="$(ruby -e "puts (1..$SIZE).to_a.shuffle.join(' ')")";
echo "Testing with $SIZE numbers:";
NUM=$(./push_swap $ARG | wc -l);
RESULT=$(./push_swap $ARG | ./checker_Mac $ARG);
echo "Operations: $NUM";
echo "Result: $RESULT"
```

### 📊 Operation Count Validator
```bash
# Function to test and validate operation counts
test_push_swap() {
    SIZE=$1
    MAX_OPS=$2
    ARG="$(ruby -e "puts (1..$SIZE).to_a.shuffle.join(' ')")";
    OPS=$(./push_swap $ARG | wc -l | tr -d ' ');
    RESULT=$(./push_swap $ARG | ./checker_Mac $ARG);
    
    echo "\nTesting $SIZE numbers:";
    echo "Operations: $OPS";
    echo "Result: $RESULT";
    
    if [ "$RESULT" != "OK" ]; then
        echo "❌ Failed: Not properly sorted";
    elif [ $OPS -gt $MAX_OPS ]; then
        echo "⚠️ Warning: Used $OPS operations (max allowed: $MAX_OPS)";
    else
        echo "✅ Success: Used $OPS operations (max allowed: $MAX_OPS)";
    fi
}

# Run tests for different sizes with their respective limits
test_push_swap 3 3
test_push_swap 5 12
test_push_swap 100 700
test_push_swap 500 5500
```

### 🚨 Common Edge Cases
```bash
# Test with three numbers in all possible combinations
for i in {1..3}; do
    for j in {1..3}; do
        for k in {1..3}; do
            if [ $i -ne $j ] && [ $j -ne $k ] && [ $i -ne $k ]; then
                echo "\nTesting combination: $i $j $k";
                ./push_swap $i $j $k | wc -l;
                ./push_swap $i $j $k | ./checker_Mac $i $j $k;
            fi
        done
    done
done

# Test with problematic sequences
CASES=(
    "2 1 3 6 5 8"
    "1 5 2 4 3"
    "0 1 2 3 4 5 -1"
    "999999 -999999 0 1 -1"
)

for case in "${CASES[@]}"; do
    echo "\nTesting: $case";
    ./push_swap $case | wc -l;
    ./push_swap $case | ./checker_Mac $case;
done
```

These test commands will help you ensure your push_swap:
- Handles all edge cases correctly
- Performs within operation limits
- Sorts correctly in all scenarios
- Manages memory properly under stress
- Handles various input sizes efficiently

Remember to:
1. Have your `push_swap` and `checker_Mac` executables in the current directory
2. Make sure Ruby is installed for random number generation
3. Copy the entire function block for the operation count validator to use it
