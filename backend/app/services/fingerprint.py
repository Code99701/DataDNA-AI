import uuid
import hashlib

# Step 1: Generate unique fingerprint
def generate_fingerprint():
    return str(uuid.uuid4())


# Step 2: Convert text → binary
def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)


# Step 3: Hash fingerprint (SHA256)
def hash_fingerprint(fingerprint):
    return hashlib.sha256(fingerprint.encode()).hexdigest()


# Step 4: Full pipeline (DataDNA)
def create_datadna():
    fingerprint = generate_fingerprint()
    
    # Optional: add end marker for safe extraction
    fingerprint_with_marker = fingerprint + "###"
    
    binary = text_to_binary(fingerprint_with_marker)
    hashed = hash_fingerprint(fingerprint)

    return {
        "fingerprint": fingerprint,
        "binary": binary,
        "hash": hashed
    }