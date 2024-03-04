from lib.keygen import Keygen
from lib.crypt import Crypt

keygen = Keygen()
pk = keygen.getPublicKey()
sk = keygen.getSecretKey()

print(f'public: {pk}')
print(f'secret: {sk}')

crypt = Crypt()

message = 'Я шифрую по алгоритму RSA'
encoded = crypt.encode(pk, message)
print (encoded)

decoded = crypt.decode(sk, encoded)
print (decoded)