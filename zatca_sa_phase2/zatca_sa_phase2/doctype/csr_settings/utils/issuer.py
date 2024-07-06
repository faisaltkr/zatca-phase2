from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Generate a self-signed X.509 certificate (example)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

# Generate a key pair
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)


def generate_issue_details(
        country,state,locality,on,cn
):
    subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, country),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME,state),
    x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, on),
    x509.NameAttribute(NameOID.COMMON_NAME, cn),
    ])
    issuer_name = issuer.rfc4514_string()
    serial_number = x509.random_serial_number()

    # Extract issuer name and serial number
    issuer_name_str = issuer_name
    serial_number_str = serial_number

    return issuer_name_str,serial_number_str