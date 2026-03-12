MOVES = [["R", "L", "F", "B", "U", "D"], ["M", "S", "E", "x", "y", "z"] ]
IGNORED_CHARS= "(){}[]"
def verifyAlg(alg: str):
    isValid = True
    algStr=alg
    for i in IGNORED_CHARS:
        algStr = algStr.replace(i, "")
    isComm = "," in algStr
    commaCount = 0
    colonCount = 0
    algList = algStr.split()
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
                elif j == move[-1] and j == ",":
                    commaCount += 1
                elif j == move[-1] and j == ":":
                    colonCount += 1
                else:
                    isValid= False
                    break
        if colonCount > 1 or commaCount > 1 or commaCount > colonCount:
            isValid = False
        if not isValid:
            break
    return isValid

def test():
    pass


