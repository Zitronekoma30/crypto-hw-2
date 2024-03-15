from reedsolo import RSCodec, ReedSolomonError
import random
rsc = RSCodec(50)

def generate_random_128_bits():
    # generate a random 128 long list of True / False values
    return [random.choice([True, False]) for _ in range(128)]


def xor(bio, ekey):
    fuzzy = ekey.copy()
    for i in range(len(bio)):
        if bio[i] != ekey[i]:
            fuzzy[i] = True
        else:
            fuzzy[i] = False
    return fuzzy

def bytearray_to_bool_array(byte_array):
    bool_array = []
    for bit in byte_array:
        if bit == True:
            bool_array.append(True)
        else:
            bool_array.append(False)
    return bool_array

def decode(fuzzy, bio_dec):
    fuzzy = xor(bio_dec, fuzzy)
    try:
        out, code, errs = rsc.decode(fuzzy)
        out = bytearray_to_bool_array(out)
        return out
    except ReedSolomonError as e:
        print("Could not decode the message")
        return

def encode(key, bio_enc):
    ekey = rsc.encode(key)
    fuzzy = xor(bio_enc, ekey)
    return fuzzy

def burst_error(bits, chance, length_range):
    for i in range(len(bits)):
        if random.random() < chance:
            length = random.randint(length_range[0], length_range[1])
            for j in range(length):
                if i + j < len(bits):
                    bits[i + j] = not bits[i + j]
    return bits

def evenly_distributed_error(bits, chance):
    for i in range(len(bits)):
        if random.random() < chance:
            bits[i] = not bits[i]
    return bits


def encode_decode_test(type, chance, len_range):
    key = generate_random_128_bits()
    bio_enc = generate_random_128_bits()
    bio_dec = bio_enc

    fuzzy = encode(key, bio_enc)
    
    # corrput bio_dec
    if type == "even":
        bio_dec = evenly_distributed_error(bio_dec, 0.15)
    elif type == "burst":
        bio_dec = burst_error(bio_dec, 0.02, [3, 5])

    out = decode(fuzzy, bio_dec)
    
    if out == key:
        return True
    return False
