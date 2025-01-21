from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_rsa_keys():
    """Generate RSA Keys and storage it into DB"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),  # Use a passphrase if needed
    )

    public_key = private_key.public_key()

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_key_pem, public_key_pem


# Generate and save the keys
private_key, public_key = generate_rsa_keys()

# Save to files (optional)
with open("private_key.pem", "wb") as priv_file:
    priv_file.write(private_key)

with open("public_key.pem", "wb") as pub_file:
    pub_file.write(public_key)

print("Private Key:\n", private_key.decode())
print("Public Key:\n", public_key.decode())
