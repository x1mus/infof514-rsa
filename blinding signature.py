
def blind_signature_attack(message, public_key, private_key):
    random_factor = 42

    masked_message = (message * pow(random_factor, public_key.exponent, public_key.modulus)) % public_key.modulus

    signature = pow(masked_message, private_key.exponent, private_key.modulus)

    unmasked_signature = pow(signature, private_key.exponent, private_key.modulus)

    return unmasked_signature


class Key:
    def __init__(self,  modulus, exponent):
        self.modulus = modulus
        self.exponent = exponent



# Example of usage
message = 12345
# Exemple for public and private key (exponent, modulus)
public_key = Key( 100019, 65537)
private_key = Key( 100019, 40873)

unmasked_signature = blind_signature_attack(message, public_key, private_key)
print("Unmasked sigature:", unmasked_signature)
