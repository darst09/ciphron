class Converter:    
    #----------------------------------
    #перевод текста в строку шестнадцатиричный формат    
    #----------------------------------
    def textToHex(self, sText):
        utf8 = sText.encode("utf-8")
        sHex = utf8.hex()
        return sHex
    
    #----------------------------------
    #перевод строки в шестнадцатиричном формате в текста    
    #----------------------------------    
    def hexToText(self, sHex):
        utf8 = bytes.fromhex(sHex)
        sText = utf8.decode('utf-8')
        return sText