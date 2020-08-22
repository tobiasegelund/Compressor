
import sys
import PQHeap
from Element import Element
from bitIO import BitReader
from Encode import huffman


with open(file=str(sys.argv[2]), mode="wb") as decodedFile:
# Åbner den komprimeret fil
    with open(file=str(sys.argv[1]), mode="rb") as compressedfile:

        reader = BitReader(compressedfile)

        elements = []

        for i in range(256):

            bites = reader.readint32bits()

            z = Element(bites, i)
            PQHeap.insert(elements, z)

        huffmanTree = huffman(elements)


        bytesTotal = huffmanTree.key

        extractedData = huffmanTree.data

        bytesCount = 0


        while bytesCount < bytesTotal:

            bit = reader.readbit()

            temp = extractedData[bit]

            while isinstance(temp, int) is not True:

                bit = reader.readbit()

                temp = temp[bit]

            bytesCount += 1
            decodedFile.write(bytes([temp]))
