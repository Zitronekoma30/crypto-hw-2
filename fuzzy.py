from reedsolo import RSCodec, ReedSolomonError
import random
import matplotlib.pyplot as plt
import numpy as np

rsc = RSCodec(40)

def generate_random_128_bits():
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
        bio_dec = evenly_distributed_error(bio_dec, chance)
    elif type == "burst":
        bio_dec = burst_error(bio_dec, chance, len_range)
    elif type == "random":
        bio_dec = generate_random_128_bits()

    out = decode(fuzzy, bio_dec)
    
    if out == key:
        return True
    return False

def plot_test_runs(type):
    chances = []
    precentage_success = []

    samples = 30

    for i in range(0, 100, 1):
        chance = i/100
        #print(chance)
        chances.append(chance)
        successes = 0
        for j in range(samples):
            if encode_decode_test(type, chance, [12, 20]) == True:
                successes += 1
                #print("Success")
        precentage_success.append(successes/samples)
        if successes/samples == 0:
            return chance

    plt.plot(chances, precentage_success)
    plt.xlabel('Chance of error')
    plt.ylabel('Precentage of successful decodes')
    plt.show()

plot_test_runs("random")
#print(encode_decode_test("random", 0.1, [3, 5]))

def find_point_of_failure():
    length = [0, 5]
    chance = []
    upper_burst = []
    for i in range(0, 20, 1):
        length[0] += 5
        length[1] += 5
        chance.append(plot_test_runs("burst"))
        upper_burst.append(length[1])
    plt.plot(upper_burst, chance, 'o')

    # calculate the trend line
    z = np.polyfit(upper_burst, chance, 1)
    p = np.poly1d(z)

    # plot the trend line
    plt.plot(upper_burst, p(upper_burst), "r--")

    plt.xlabel('Length of burst error')
    plt.ylabel('Maximum chance of successful decode')
    plt.show()

#find_point_of_failure()