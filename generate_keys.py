import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def save_key_to_file(path, key, is_private=False):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Save the key to a file
    with open(path, 'wb') as key_file:
        if is_private:
            # Serialize the private key
            key_file.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ))
        else:
            # Serialize the public key
            key_file.write(key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ))


if __name__ == '__main__':
    # Directory where keys will be saved
    base_directory = r'./users/'  # Modify this path to suit your needs

    # Generate keys for Alice
    alice_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    alice_public_key = alice_private_key.public_key()

    # Save Alice's private and public keys to respective files
    save_key_to_file(os.path.join(base_directory, 'alice', 'private_key.txt'), alice_private_key, is_private=True)
    save_key_to_file(os.path.join(base_directory, 'alice', 'public_key.txt'), alice_public_key, is_private=False)

    # Generate keys for Bob
    bob_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    bob_public_key = bob_private_key.public_key()

    # Save Bob's private and public keys to respective files
    save_key_to_file(os.path.join(base_directory, 'bob', 'private_key.txt'), bob_private_key, is_private=True)
    save_key_to_file(os.path.join(base_directory, 'bob', 'public_key.txt'), bob_public_key, is_private=False)

    # Generate keys for Charlie
    charlie_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    charlie_public_key = charlie_private_key.public_key()

    # Save Charlie's private and public keys to respective files
    save_key_to_file(os.path.join(base_directory, 'charlie', 'private_key.txt'), charlie_private_key, is_private=True)
    save_key_to_file(os.path.join(base_directory, 'charlie', 'public_key.txt'), charlie_public_key, is_private=False)
