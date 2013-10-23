import sys

from LanguageCheck import Trigram
def testFile(fileName): 
    reader = open(fileName)
    all_texts = reader.read().splitlines()
    EngCount = 0
    nEngCount = 0
    counter = 0
    for line in all_texts:
        counter = counter + 1
        retVal = testText(line, counter)
        if retVal == 1:
            EngCount = EngCount + 1
        else:
            nEngCount = nEngCount + 1
    print str(EngCount) + " English Text Detected\n"
    print str(nEngCount) + " Non-English Text Detected"

def testText(text, counter): 
    unknown = Trigram(text)
    y = unknown.isEnglish()
    x = unknown.enSimilarity
    if y:
        print("sentence " + str(counter) + " is in English with similarity of " + str(x))
        return 1
    else:
        print("sentence " + str(counter) + " is not in English with similarity of " + str(x))
        return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "no parameter specified!!"
        print "The correct command python tester.py -f fileName"
    elif sys.argv[1] == "-f" and len(sys.argv) == 3:
        testFile(sys.argv[2])
    else:
        print "Incorrect input format!!"
        print "The correct command python tester.py -f fileName"
