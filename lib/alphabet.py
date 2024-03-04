class Alphabet:

    #----------------------------------
    #алфавит для шифрования    
    #----------------------------------
    def getAlphabet(self):
        aExt = '*@#$%^&{}()/.,!?:;-"+-='
        aEn = 'abcdefghijklmnopqrstuvwxyz'
        aEnUp = aEn.upper()
        aRu = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
        aRuUp = aRu.upper()
        aNum = '0123456789'
        aSpace = ' '   

        return aExt + aNum + aEn +aEnUp + aRu + aRuUp + aSpace;
    
    #----------------------------------
    #получение кодов букв для сообщения
    #----------------------------------
    def getCodes(self, message):
        a = self.getAlphabet();

        codes = [];    
        for x in message:
            #если символ отсутствует в алфавите он будет удален из сообщения
            if x in a:
                codes.append(a.index(x))
            
        return codes        