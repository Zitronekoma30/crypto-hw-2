from reedsolo import RSCodec, ReedSolomonError
import random
rsc = RSCodec(10)

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

def main():
    key = [True, False, True, True, False, True]#generate_random_128_bits()
    ekey = rsc.encode(key)
    bio_enc = [False, True, True, False, True, False] #generate_random_128_bits()
    bio_dec = [False, False, True, False, True, False]

    fuzzy = xor(bio_enc, ekey)
    #print(fuzzy)
    fuzzy = xor(bio_dec, fuzzy)

    try:
        out, other1, other2 = rsc.decode(fuzzy)
        out = bytearray_to_bool_array(out)
    except ReedSolomonError as e:
        print("Could not decode the message")
        return
    
    print(key)
    print(out)
    if out == key:
        print("Success")


main()