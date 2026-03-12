import json 
import csv 
import os
import cubehandling as cube
from pathlib import Path
dataDir = Path.home() / ".3s-trainer" 
dataDir.mkdir(parents = True, exist_ok = True)
pairData = dataDir / "pairs.json"
LETTERS = [chr(i) for i in range(65, 89)]

def readPair():
    with open(pairData, mode="r", encoding="utf-8") as readFile:
        originalData = readFile.read()
    return json.loads(originalData)

def writePair(data):
    with open(pairData, mode = "w", encoding="utf-8") as writeFile:
        writeFile.write(json.dumps(data, indent=4, separators=(",", ":")))

def strPiece(pieceTypeIn):
    return "edges" if pieceTypeIn else "corners"

def fetchPair(letters, pieceTypeIn):
    pieceType = strPiece(pieceTypeIn)
    pairsParsed = readPair()
    return [pairsParsed[pieceType][letters]["commutator"], pairsParsed[pieceType][letters]["word"]]
    
def addPair(pieceTypeIn, letters, comm, word):
    pieceType = "edges" if pieceTypeIn else "corners"
    pairsParsed =  readPair()
    pairsParsed[pieceType][letters] = {
        "commutator": comm,
        "word": word,
    }
    writePair(pairsParsed)
def initiatePairs(): 
    if (not pairData.exists()) or pairData.stat().st_size == 0:
        print("file created")
        pairData.write_text(json.dumps({}))
    with open(pairData, mode="r", encoding="utf-8") as readFile:
        originalData = readFile.read()
    pairsParsed = json.loads(originalData)
    #print(json.dumps(pairsParsed))
    if not "initiated" in pairsParsed:
        print("initiated")
        pairsParsed = {"initiated": "yes", "corners": {}, "edges": {}}
        for i in LETTERS:
            for j in LETTERS:
                letters = i + j
                if not i == j:
                    pairsParsed["edges"][letters] = {
                        "commutator": '',
                        "word": '',
                    }
                    pairsParsed["corners"][letters] = {
                        "commutator": '',
                        "word": '',
                    }
    with open(pairData, mode = "w", encoding="utf-8") as writeFile:
        writeFile.write(json.dumps(pairsParsed, indent=4, separators=(",", ":")))
def resetPairs(dataType):
    pairsParsed = readPair()
    for i in LETTERS:
        for j in LETTERS:
            letters = i+j
            if not i == j:
                pairsParsed["edges"][letters][dataType] = ''
                pairsParsed["corners"][letters][dataType] = ''
    writePair(pairsParsed)
    return
def importCsv(filePath, pieceTypeIn, dataType):
    badPairs = ""
    pieceType = strPiece(pieceTypeIn)
    with open (filePath, newline = '') as csvfile:
        data = list(csv.reader(csvfile))
    pairsParsed = readPair()
    for i in range(len(LETTERS)):
        for j in range(len(LETTERS)):
            letters = LETTERS[i] + LETTERS[j]
            if not i == j:
                success = cube.verifyAlg(data[j+1][i+1])
                if success or dataType == "word":
                    pairsParsed[pieceType][letters][dataType] = data[j+1][i+1]
                    print(letters + ': ', data[j+1][i+1])
                else:
                    badPairs += letters + ", "
    writePair(pairsParsed)
    return badPairs

    
