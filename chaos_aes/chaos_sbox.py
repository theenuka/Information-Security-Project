from hashlib import sha256

#seed from key
def seed_from_key(key: bytes) -> float:
    digest = sha256(key).digest()       #hash the key and get uniform looking key value
    value = int.from_bytes(digest[:8], "big") / 2**64    #take the first 8 bytes(SHA256 256 bits-32 bytes)
    return min(max(value, 1e-12), 1 - 1e-12)     #convert 8 bytes to big integer

#logistic map
def logistic_values(seed: float, count: int = 256, r: float = 3.99, warmup: int = 512) -> list[float]:     #generate 256 values 
    x = seed
    for _ in range(warmup):    #run logistic map 512 times  without store output to stabilize chaotic behavior
        x = r * x * (1 - x)
    out = []
    for _ in range(count):
        x = r * x * (1 - x)
        out.append(x)    #generate and return 256 output values
    return out

#create valid s-box
def make_sbox(key: bytes) -> list[int]:     #input make_sbox function as a key and return integer list
    values = logistic_values(seed_from_key(key))   #seed from key and generate 256 logistic values
    sbox = [i for i, _ in sorted(enumerate(values), key=lambda p: p[1])]                  #pair index and value and sort
    if sorted(sbox) != list(range(256)):
        raise ValueError("Generated S-Box is not bijective")   #whether the generated sbox is a valid permutation of 0-255(bijective)
    return sbox

#inverse s-box for decryption
def inverse_sbox(sbox: list[int]) -> list[int]:   #since s-box is bijective, construct inverse s-box by reverse mapping
    inv = [0] * 256
    for i, v in enumerate(sbox):
        inv[v] = i
    return inv
