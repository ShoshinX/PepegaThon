from base64 import b64decode, b64encode
import ecdsa


def verify_sign(public_key, cleartext, encrypted):
    """
    public_key and encrypted are base64 encoded strings.
    encrypted is the entire cleartext string but encrypted with
    the user's private_key.
    return: Boolean. True if the signature is valid; False otherwise. 
    """
    vk = ecdsa.VerifyingKey.from_string(b64decode(public_key.encode()))
    return vk.verify(b64encode(encrypted), cleartext.encode())
