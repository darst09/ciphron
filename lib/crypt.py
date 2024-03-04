from lib.alphabet import Alphabet
from lib.converter import Converter

class Crypt:
    
    #----------------------------------
    #шифрование сообщения с помощью публичного ключа
    #----------------------------------
    def encode(self, pk, message):
        #получим e, n компоненты публичного ключа
        if self.isKeyValid(pk):
            e, n = self.__getKey(pk)
        else:
            return None
                
        alphabet = Alphabet()       
        #получаем коды букв сообщения относительно нашего алфавита
        codes = alphabet.getCodes(message)
        
        #сюда будем складывать коды в зашифрованном виде
        encoded = []
        
        prev = 0;
        for c in codes:
            #сначала "спрячем" явно определенный код символа
            #для этого применим дополнительное правило: каждый следующий код увеличим на сумму предыдущих 
            #таким образом каждая предыдущая часть сообщения влияет на следующую                        
            cLocked = (c + prev) % n
            prev = cLocked
        
            #зашифруем полученный "спрятаный" код символа публичным ключом
            cEncoded = cLocked**e % n            

            #добавим зашифрованный код в массив         
            encoded.append(str(cEncoded))
        
        #получим строку кодов разделенную запятыми
        sEncoded = ",".join(encoded)
                          
        #возвращаем строку с кодами в шестнадцатиричном формате
        #чтобы сделать результат кодирования еще более не явным
        converter = Converter()      
          
        return converter.textToHex(sEncoded)
            
    
    #----------------------------------
    #расшифровка сообщение с помощью секретного ключа
    #----------------------------------
    def decode(self, sk, sHex):
        #получим d, n компоненты секретного ключа
        if self.isKeyValid(sk):
            d, n = self.__getKey(sk)
        else:
            return None
        
        alphabet = Alphabet()
        letters = alphabet.getAlphabet()
        
        converter = Converter()        
        #закодированнное сообщение переведем из шестнадцатиричного формата в текст
        #получим строку зашифрованных кодов, разделенную запятыми
        sEncoded = converter.hexToText(sHex)
        #превратим эту строку в массив чисел
        encoded = [int(x) for x in sEncoded.split(',')]
            
        #сюда будем складывать дешифрованные символы    
        decoded = []
        
        prev = 0
        for c in encoded:
            #каждый зашифрованный код расшифруем с помощью секретного ключа
            cDecoded = c**d % n                       
            
            #далее нужно получить "явный" код 
            #применяем обратное правило для "спрятанного" кода
            #то есть из каждого следующего кода вычтем сумму предыдущих
            cUnlocked = (cDecoded - prev) % n
            prev = cDecoded
        
            #если код символа есть в алфавите, 
            #то добавляем букву, соотвествующую коду в массив расшифровки
            #иначе пропускаем этот код
            try:
                decoded.append(letters[cUnlocked])
            except IndexError:
                continue
        
        #все буквы, из массива расшифровки склеиваем в строку             
        return "".join(decoded)


    #----------------------------------
    #проверка ключа 
    #ключ должен быть представлен в шестнадцатиричном формате
    #----------------------------------    
    def isKeyValid(self, sHash):
        try:
            a, b = self.__getKey(sHash)
            return True
        except ValueError:
            return False        
    

    #----------------------------------
    #получение компонентов ключа из ключа в шестнадцатиричном формате
    #----------------------------------    
    def __getKey(self, sHash):
        converter = Converter()
        sKey = converter.hexToText(sHash)
        a, b = sKey.split(',')
        return int(a), int(b)