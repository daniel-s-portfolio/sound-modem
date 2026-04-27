
def main():
    #read in message.wav

    #decode message.wav

    #save decoded text as message.txt
    pass

def calc_tone_power(samples, num_samples, f, fs):
    i = 0
    q = 0
    for n in range(0, num_samples):
        angle = 2 * math.pi * f * n / fs
        i += samples[n] * math.cos(angle)
        q += samples[n] * math.sin(angle)
    return (i ** 2) + (q ** 2)


if __name__ == "__main__":
    main()
