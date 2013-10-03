from LanguageCheck import Trigram

def test():
    y = 0
    f = open('FinnishTest.txt')
    for z, line in enumerate(f):        
        unknown = Trigram(line)
        value = unknown.isEnglish()
        if value:
            #y = y+1       
            print('text' + str(z) + ' is in English')
        else:
            y = y+1
            print('text' + str(z) + ' is not in')
    print("%s correct detection" %y)
    acc = y/z
    print("accuracy %f %%" %(acc*100))

if __name__ == '__main__':
    test()
