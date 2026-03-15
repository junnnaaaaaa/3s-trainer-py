import cubehandling as cube
# Basic commutator [A, B]
print("Test 1 value: " + str(cube.verifyAlg("R U R' , U' R U")) + "   Expected Value: True")
print("Test 2 value: " + str(cube.verifyAlg("R , U")) + "   Expected Value: True")

# Conjugate / setup moves [setup : A, B]
print("Test 3 value: " + str(cube.verifyAlg("R U : R' , U'")) + "   Expected Value: True")
print("Test 4 value: " + str(cube.verifyAlg("R : U , R'")) + "   Expected Value: True")

# Colon without comma (invalid - setup must have a commutator)
print("Test 5 value: " + str(cube.verifyAlg("R U : R' U'")) + "   Expected Value: False")

# Multiple commas (invalid)
print("Test 6 value: " + str(cube.verifyAlg("R , U , R'")) + "   Expected Value: False")

# Multiple colons (invalid)
print("Test 7 value: " + str(cube.verifyAlg("R : U : R' , U'")) + "   Expected Value: False")

# Comma without setup (valid - plain commutator)
print("Test 8 value: " + str(cube.verifyAlg("R U R' , U' R U R'")) + "   Expected Value: True")

# With brackets ignored
print("Test 9 value: " + str(cube.verifyAlg("[R U : R' , U']")) + "   Expected Value: True")
print("Test 10 value: " + str(cube.verifyAlg("[R , U]")) + "   Expected Value: True")

# Invalid move inside commutator
print("Test 11 value: " + str(cube.verifyAlg("Q , U")) + "   Expected Value: False")
print("Test 12 value: " + str(cube.verifyAlg("R : Q , U")) + "   Expected Value: False")

# Colon and comma on same move token (edge case)
print("Test 13 value: " + str(cube.verifyAlg("R: U ,R'")) + "   Expected Value: True")

# Empty setup before colon
print("Test 14 value: " + str(cube.verifyAlg(": R , U")) + "   Expected Value: False")

# Comma at start (invalid)
print("Test 15 value: " + str(cube.verifyAlg(", R U")) + "   Expected Value: False")
