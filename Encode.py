import sys
import PQHeap
from Element import Element
from bitIO import BitWriter

def huffman(C):
    n = len(C)

    Q = C

    for i in range(n - 1):

        x = PQHeap.extractMin(Q)
        y = PQHeap.extractMin(Q)

        xExtractedKey = x.key
        xExtractedData = x.data

        yExtractedKey = y.key
        yExtractedData = y.data

        freq = xExtractedKey + yExtractedKey

        z = Element(int(freq), [xExtractedData, yExtractedData])


        PQHeap.insert(Q, z)


    return PQHeap.extractMin(Q)



def codeWords(T, pathway, listOfCodes):


    if isinstance(T, int) is not True:

        codeWords(T=T[0], pathway=pathway + "0", listOfCodes=listOfCodes)

        codeWords(T=T[1], pathway=pathway + "1", listOfCodes=listOfCodes)

    else:

        listOfCodes[T] = pathway


if __name__ == "__main__":

    with open(file=str(sys.argv[1]), mode="rb") as inputFile:

        freqTable = [0] * 256

        elements = []

        byte = inputFile.read(1)
        while byte:
            byteNumber = byte[0]

            freqTable[byteNumber] += 1

            byte = inputFile.read(1)

        for byteIndex in range(len(freqTable)):
            z = Element(freqTable[byteIndex], byteIndex)
            PQHeap.insert(elements, z)


        huffmanTree = huffman(elements)


        extractedData = huffmanTree.data

        codes = [0] * 256
        codeWords(T=extractedData, pathway="", listOfCodes=codes)


    with open(file=sys.argv[2], mode="wb") as compressedFile:

        with BitWriter(compressedFile) as writer:

            for freqByte in freqTable:

                writer.writeint32bits(freqByte)


            with open(file=str(sys.argv[1]), mode="rb") as inputFile:


                byte = inputFile.read(1)


                while byte:

                    byteNumber = byte[0]

                    codePath = codes[byteNumber]

                    for bit in codePath:
                        writer.writebit(int(bit))


                    byte = inputFile.read(1)
