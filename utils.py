from cryptography.hazmat.primitives import serialization


def load_key_from_file(path, is_private=False):
    # Read the key from the file
    with open(path, 'rb') as key_file:
        if is_private:
            # Deserialize the private key
            return serialization.load_pem_private_key(
                key_file.read(),
                password=None,  # If the private key is encrypted, provide the password
            )
        else:
            # Deserialize the public key
            return serialization.load_pem_public_key(
                key_file.read()
            )
