MOVES = [["R", "L", "F", "B", "U", "D"], ["M", "S", "E", "x", "y", "z"] ]
IGNORED_CHARS= "(){}[]"
def verifyAlg(alg: str):
    isValid = True
    algStr=alg
    for i in IGNORED_CHARS:
        algStr = algStr.replace(i, "")
    isComm = "," in algStr
    algList = algStr.split()
    if not isComm:
        for i in algList:
            isFaceMove = False
            isWide = False
            isPrime = False
            isDouble = False
            move = list(i)
            if move[0] in MOVES[0]:
                isFaceMove = True
            elif move[0].upper() in MOVES[0]:
                isFaceMove = True
                isWide = True
            elif move[0] in MOVES[1]:
                isFaceMove = False
            else:
                isValid = False
                break
            if len(i) > 1:
                for j in move[1:]:
                    if j == "2" and not isDouble:
                         isDouble = True
                    elif j == "w" and isFaceMove and not isWide:
                        isWide= True
                    elif j == "'" and not isPrime:
                        isPrime = True
                    else:
                        isValid= False
                        break
            if not isValid:
                break
    return isValid

def test():
   # Basic Valid Moves
    print("Test 1 value: " + str(verifyAlg("R")) + "   Expected Value: True")
    print("Test 2 value: " + str(verifyAlg("L")) + "   Expected Value: True")
    print("Test 3 value: " + str(verifyAlg("F")) + "   Expected Value: True")
    print("Test 4 value: " + str(verifyAlg("B")) + "   Expected Value: True")
    print("Test 5 value: " + str(verifyAlg("U")) + "   Expected Value: True")
    print("Test 6 value: " + str(verifyAlg("D")) + "   Expected Value: True")

# Slice / Rotation Moves
    print("Test 7 value: " + str(verifyAlg("M")) + "   Expected Value: True")
    print("Test 8 value: " + str(verifyAlg("S")) + "   Expected Value: True")
    print("Test 9 value: " + str(verifyAlg("E")) + "   Expected Value: True")
    print("Test 10 value: " + str(verifyAlg("x")) + "   Expected Value: True")
    print("Test 11 value: " + str(verifyAlg("y")) + "   Expected Value: True")
    print("Test 12 value: " + str(verifyAlg("z")) + "   Expected Value: True")

# Modifiers
    print("Test 13 value: " + str(verifyAlg("R'")) + "   Expected Value: True")
    print("Test 14 value: " + str(verifyAlg("R2")) + "   Expected Value: True")
    print("Test 15 value: " + str(verifyAlg("Rw")) + "   Expected Value: True")
    print("Test 16 value: " + str(verifyAlg("r")) + "   Expected Value: True")

# Multi-Move Algorithms
    print("Test 17 value: " + str(verifyAlg("R U R' U'")) + "   Expected Value: True")
    print("Test 18 value: " + str(verifyAlg("R U R' U R U2 R'")) + "   Expected Value: True")
    print("Test 19 value: " + str(verifyAlg("R U R' F' R U R' U' R' F R2 U' R'")) + "   Expected Value: True")

# Commutators (any string with ',' is valid)
    print("Test 20 value: " + str(verifyAlg("R, U")) + "   Expected Value: True")
    print("Test 21 value: " + str(verifyAlg("[R, U]")) + "   Expected Value: True")

# Ignored Characters
    print("Test 22 value: " + str(verifyAlg("(R U R' U')")) + "   Expected Value: True")
    print("Test 23 value: " + str(verifyAlg("{R U}")) + "   Expected Value: True")
    print("Test 24 value: " + str(verifyAlg("[R U]")) + "   Expected Value: True")

# Empty String
    print("Test 25 value: " + str(verifyAlg("")) + "   Expected Value: True")

# Invalid Move Letters
    print("Test 26 value: " + str(verifyAlg("Q")) + "   Expected Value: False")
    print("Test 27 value: " + str(verifyAlg("A")) + "   Expected Value: False")
    print("Test 28 value: " + str(verifyAlg("R U Q U'")) + "   Expected Value: False")
    print("Test 29 value: " + str(verifyAlg("3")) + "   Expected Value: False")
    print("Test 30 value: " + str(verifyAlg("R @ U")) + "   Expected Value: False")

# Invalid Repeated Modifiers (currently bugged - will return True)
    print("Test 31 value: " + str(verifyAlg("R''")) + "   Expected Value: False")
    print("Test 32 value: " + str(verifyAlg("R22")) + "   Expected Value: False")
    print("Test 33 value: " + str(verifyAlg("R2'")) + "   Expected Value: False")

# Wide modifier on slice move
    print("Test 34 value: " + str(verifyAlg("Mw")) + "   Expected Value: False")

test()
