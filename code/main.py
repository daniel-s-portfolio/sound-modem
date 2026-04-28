import numpy as np
from scipy.io import wavfile

BAUD = 300 # bits/second
SAMPLES_PER_BIT = 160  # 48000 samples/sec / 300 bits/second
FREQ_SPACE = 2025
FREQ_MARK = 2225


def main():
    # read in message.wav, decode it, write message to file
    sample_rate, samples = load_wav("message.wav")
    message = decode_wav(sample_rate, samples)
    f = open("MESSAGE.txt", "w")
    f.write(message)


def load_wav(filename):
    """
    Reads in a .wav file, converts to float representation -1 to 1, returns sample rate and samples
    """
    sample_rate, data = wavfile.read(filename)
    
    # ensure data is float from -1 to 1
    if data.dtype == np.int16:
        samples = data.astype(np.float32) / 32768.0
    else:
        samples = data.astype(np.float32)
    return sample_rate, samples


def decode_wav(sample_rate, samples):
    """
    Calculates power at 2025hz and 2225hz, using the higher power at each sample block.  If
    2225hz is higher, sets bit to 1, else sets it to 0.  Then iterates through this sequence of bits in
    10-bit frames that each contain 8 data bits, converts LSB-first to MSB-first format, and creates
    a decoded ASCII message from the values represented by data bits.  Returns the message text string.
    """
    # compute reference arrays (sine for I, cosine for Q)
    t = np.arange(SAMPLES_PER_BIT) / sample_rate
    ref_space_cos = np.cos(2 * np.pi * FREQ_SPACE * t)
    ref_space_sin = np.sin(2 * np.pi * FREQ_SPACE * t)
    ref_mark_cos = np.cos(2 * np.pi * FREQ_MARK * t)
    ref_mark_sin = np.sin(2 * np.pi * FREQ_MARK * t)

    # process sample blocks from .wav file
    bits = []
    for i in range(0, len(samples) - SAMPLES_PER_BIT + 1, SAMPLES_PER_BIT):
        block = samples[i : i + SAMPLES_PER_BIT]
        
        # calculate power for 2025 hz
        p_space = np.dot(block, ref_space_cos)**2 + np.dot(block, ref_space_sin)**2
        # calculate power for 2225 hz
        p_mark = np.dot(block, ref_mark_cos)**2 + np.dot(block, ref_mark_sin)**2
        
        if p_mark > p_space:
            bits.append(1)
        else:
            bits.append(0)

    # group into 10-bit frames
    message = ""
    for i in range(0, len(bits) - 9, 10):
        frame = bits[i : i + 10]
        data_bits = frame[1:9] # data is in the middle 8 bits of frame
        
        # convert bit list to integer.  extract the index and bit value from the data bits,
        # then left shift the bits by index value to convert them from the LSB-first format into MSB-first
        char_code = 0
        for bit_index, bit_value in enumerate(data_bits):
            char_code |= (bit_value << bit_index)
            
        message += chr(char_code) # map integer to ASCII and append to message string
    
    return message


if __name__ == "__main__":
    main()
