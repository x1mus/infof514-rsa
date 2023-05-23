

from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

class Oracle:
    def __init__(self):
        self.key = RSA.generate(1024)
        self.modulus = self.key.n
        self.exponent = self.key.e
    
    def get_key(self):
        return (self.key.e, self.key.n)
    
    def sign(self, message):

        result = {
            "n": self.modulus,
            "e": self.exponent,
            "sign": "You're not the administrator :)"
        }

        if b"admin" not in long_to_bytes(message).lower():
            result["sign"] = pow(message, self.key.d, self.key.n)
        
        return result


"""
# Example of usage
message = "I am the Administrator!"
# Exemple for public and private key (exponent, modulus)
public_key = Key( 100019, 65537)
private_key = Key( 100019, 40873)

unmasked_signature = blind_signature_attack(message, public_key, private_key)
print("Unmasked sigature:", unmasked_signature)
"""

# Example of usage

oracle = Oracle()
key = oracle.get_key()

message = b"I am the Administrator!"
answer = oracle.sign(bytes_to_long(message))
try:
    pow(answer["sign"], answer["e"], answer["n"])
    print(f"Good signature: {answer['sign']}")
except:
    print(f"{answer['sign']}")
print("---------------")

# Attack of the oracle
message = b"I am the Administrator!"
print("h")
forged_message = (bytes_to_long(message) * pow(2, key[0], key[1])) % key[1]
answer = oracle.sign(forged_message)

print(f"Good signature: {(answer['sign'] * pow(2,-1,key[1])%key[1])}")
print(f"Decryption of the signature: {long_to_bytes(pow((answer['sign'] * pow(2,-1,key[1])%key[1]), 65537, answer['n']))}")