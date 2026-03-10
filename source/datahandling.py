import json 
import csv
import os
from pathlib import Path
LETTERS = [chr(i) for i in range(65, 89)]

def addPair(data, pieceTypeIn, letters, comm, word):
    pieceType = "edges" if pieceTypeIn else "corners"
    data[pieceType][letters] = {
        "commutator": comm,
        "word": word,
    }
def initiatePairs(data): 
    if (not data.exists()) or data.stat().st_size == 0:
        print("file created")
        data.write_text(json.dumps({}))
    with open(data, mode="r", encoding="utf-8") as readFile:
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
                    addPair(pairsParsed, True, letters, '', '')
                    addPair(pairsParsed, False, letters, '', '')
    with open(data, mode = "w", encoding="utf-8") as writeFile:
        writeFile.write(json.dumps(pairsParsed, indent=4, separators=(",", ":")))

    #print(json.dumps(pairsParsed))
def main():
    dataDir = Path.home() / ".3s-trainer" 
    dataDir.mkdir(parents = True, exist_ok = True)
    pairData = dataDir / "pairs.json"
    initiatePairs(pairData)
main()
