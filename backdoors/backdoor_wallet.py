import binascii
import ecdsa
import random
from ecdsa import SigningKey, VerifyingKey

USERS = ["Alice", "Bob", "Charlie", "Dave"]

def sha256_2_string(string_to_hash):
    """ Returns the SHA256^2 hash of a given string input
    in hexadecimal format.

    Args:
        string_to_hash (str): Input string to hash twice

    Returns:
        str: Output of double-SHA256 encoded as hexadecimal string.
    """

    import hashlib
    first_sha = hashlib.sha256(string_to_hash.encode("utf8"))
    second_sha = hashlib.sha256(first_sha.digest())
    return second_sha.hexdigest()

def get_challenge_for(netid, write_to_file):
    challenge = ""
    sk = get_key(netid)
    binary_sk = bin(int(binascii.hexlify(sk.to_string()), 16))[2:]
    # pad with 0s if key has leading 0s
    while len(binary_sk) < 192:
        binary_sk = "0" + binary_sk
    for bindigit in binary_sk:
        tx_to = random.choice(USERS)
        tx_amt = random.random() * 20
        tx_str = "From Rafael to " + tx_to + " for " + str(tx_amt)
        challenge += tx_str + "; Signature: " + sign_message(tx_str, sk, bindigit) + "\n"
    open(write_to_file, "w").write(challenge)


def sign_message(message, sk, parity_bit):
    while True:
        signature = sk.sign(message.encode("utf-8"))
        hex_signature = signature.hex()
        sig_to_int = int(hex_signature, 16)
        if (sig_to_int % 2) == parity_bit:
            return hex_signature

def is_message_signed(message, hex_sig, secret_key_hex):
    # Decode signature to bytes, verify it
    try:
        signature = binascii.unhexlify(hex_sig)
        pk = SigningKey.from_string(binascii.unhexlify(secret_key_hex)).get_verifying_key()
    except binascii.Error:
        print("binascii error; invalid key")
        return False
    try:
        return pk.verify(signature, message.encode("utf-8"))
    except ecdsa.keys.BadSignatureError:
        print("signature error; invalid signature")
        return False

def verify_key(recovered_key_hex, challenge):
    for line in challenge.splitlines():
        line_challenge = line.split("; Signature: ")
        assert(len(line_challenge) == 2)
        message = line_challenge[0]
        signature = line_challenge[1]
        if not is_message_signed(message, signature, recovered_key_hex):
            return False
        print("Verified signature successfully")
    return True

def get_key_from_challenge(challenge):
    for line in challenge.splitlines():
        line_challenge = line.split("; Signature: ")
        assert(len(line_challenge) == 2)
        message = line_challenge[0]
        signature = line_challenge[1]
        print(message, signature)

    # TODO Problem 3 - Use this to reconstruct Rafael's Key

# get_challenge_for("YOUR_NETID", "challenge") - this call won't work since some code is removed
# but gives you some idea as to how the challeng was created

challenge_text = open("challenges/YOUR_NETID").read().strip()
sk = get_key_from_challenge(challenge_text)
print(verify_key(sk, challenge_text)) # should print True
