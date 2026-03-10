import json 
import csv
import os
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
                letters = i+j
                if not i == j:
                    addPair(pairsParsed, True, '', '')
                    addPair(pairsParsed, False, '', '')
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

    #print(json.dumps(pairsParsed))
