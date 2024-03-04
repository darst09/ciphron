import math
import random
from lib.converter import Converter
    
class Keygen:
    __start = 99
    
    __end = 399
        
    __rsa = {}
    
    
    def __init__(self):
        self.__rsa = self.__getBase()
        #check = (self.__rsa['d'] * self.__rsa['e']) % self.__rsa['fn']
        #print(f'check : (d*e) % fn = 1 : {check}')
        
        
    #----------------------------------
    #получение публичного ключа
    #----------------------------------    
    def getPublicKey(self):
        sKey = ",".join([str(self.__rsa['e']), str(self.__rsa['n'])])
        
        converter = Converter() 
        return converter.textToHex(sKey)
 
 
    #----------------------------------
    #получение секретного ключа
    #----------------------------------   
    def getSecretKey(self):
        sKey = ",".join([str(self.__rsa['d']), str(self.__rsa['n'])])
        
        converter = Converter()
        return converter.textToHex(sKey)

    
    #----------------------------------
    #Вычисление состовных частей ключей
    #----------------------------------         
    def __getBase(self):
        e = d = None
        
        #если, в результате вычислений e вернет None, 
        #то получим два новых случайных простых числа p и q и спова вычислим e и d
        #
        #если, в результате вычислений d вернет None (не прошел проверку (e * d) % fn == 1 или e == d), 
        #то попытаемся получить новый e (без замены p и q) и снова вычислить d            
        while e == None or d == None:           
            if (e == None) :
                #получим список простых чисел в определенном диапазоне
                simples = self.__getSimples(self.__start, self.__end)
                #получим два случайных числа p и q
                p = q = random.SystemRandom().choice(simples)
                # q должно быть отличным от q
                while p == q:
                    q = random.SystemRandom().choice(simples);
            
                #вычисляем модуль — произведение p и q    
                n = p * q
    
                #вычислим функцию Эйлера
                fn = (p - 1) * (q - 1)        
        
            #получим компонент e публичного ключа
            #если это вторая и последующие попытки получить e (e != None)
            #то начнем посик с (e - 1)
            end = (fn - 1) if e == None else (e - 1)
            e = self.__getPublicE(fn, end)
            
            if e != None:
                #получим компонент d секретного ключа                                              
                d = self.__getSecretD(e, fn)
        
        return {'n': n, 'e': e, 'd': d, 'fn': fn, 'p': p, 'q': q}

        
    #----------------------------------
    #приватный метод
    #получение компонента e открытого ключа
    #это должно быть случайное число из диапазона [3, fn - 1] 
    #взаимно простое с fn, т.е. НОД(e, fn) = 1 / gcd(e, fn) = 1
    #----------------------------------   
    def __getPublicE(self, fn, end):        
        for e in range(end, 3, -1):       
            if self.__isSimple(e) and math.gcd(e, fn) == 1:
                return e

        return None
    
    
    #----------------------------------
    #приватный метод
    #получение компонента d секретного ключа
    #для которого выполняется условие (d*e) % fn = 1
    #то есть d должно быть такое, что при умножении на e и потом после деления на fn получился остаток 1
    #----------------------------------   
    def __getSecretD(self, e, fn):       
        gcd, x, y = self.__gcdExtended(fn, e)
        if gcd == 1:
            d = y % fn
            check = (e * d) % fn
            if (d != e and check == 1):
                return d
         
        return None
    #----------------------------------
    #приватный метод
    #проверка является ли число простым
    #----------------------------------        
    def __isSimple(self, n):
        if n % 2 == 0:
            return n == 2
        d = 3
        while d * d <= n and n % d != 0:
            d += 2
            
        return d * d > n


    #----------------------------------
    #приватный метод
    #получение списка простых чисел в заданном диапазоне
    #----------------------------------   
    def __getSimples(self, start, end):
        arr = []
        for i in range(start, end + 1):
            if self.__isSimple(i):
                arr.append(i)
                
        return arr
    
    
    #----------------------------------
    #приватный метод
    #расширенный алгоритм Евклида
    #----------------------------------    
    def __gcdExtended(self, a, b):
        if b == 0:
            return a, 1, 0
        else:
            gcd, x0, y0 = self.__gcdExtended(b, a % b)
            x = y0
            y = x0 - y0 * (a // b)
            
            return gcd, x, y
        