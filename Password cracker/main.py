import hashlib
import itertools
from string import ascii_lowercase, digits
import time
from urllib.request import urlopen


def brute_force(charset, max_length, required_hash):
    time_start = time.time()
    for password_length in range(1, max_length + 1):
        for guess in itertools.product(charset, repeat=password_length):
            guess = ''.join(guess)
            guess_hash = hashlib.md5(guess.encode("utf-8")).hexdigest()
            if guess_hash == required_hash:
                time_end = time.time()
                return "Password is {}. Found in {} seconds by brute force".format(guess, (time_end - time_start))


def dictionary(required_hash):
    try:
        time_start = time.time()
        password_dictionary = urlopen(
            "https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/Top12Thousand"
            "-probable-v2.txt").read()
        password_dictionary = password_dictionary.decode("utf-8")
        password_dictionary = password_dictionary.split("\n")
        for guess in password_dictionary:
            guess_hash = hashlib.md5(guess.encode("utf-8")).hexdigest()
            if guess_hash == required_hash:
                time_end = time.time()
                return "Password is {}. Found in {} seconds in dictionary".format(guess, (time_end - time_start))
    except Exception as exception:
        print(exception)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    charset_1 = ascii_lowercase + digits  # + ascii_uppercase
    charset_2 = ascii_lowercase
    print(brute_force(charset_1, 7, "e99a18c428cb38d5f260853678922e03"))
    print(brute_force(charset_2, 7, "8d3533d75ae2c3966d7e0d4fcc69216b"))
    print(brute_force(charset_2, 7, "0d107d09f5bbe40cade3de5c71e9e9b7"))
    # print(brute_force(charset_2, 8, "5f4dcc3b5aa765d61d8327deb882cf99"))
    print("")
    print(dictionary("5f4dcc3b5aa765d61d8327deb882cf99"))
    print(dictionary("e99a18c428cb38d5f260853678922e03"))
    print(dictionary("8d3533d75ae2c3966d7e0d4fcc69216b"))
    print(dictionary("0d107d09f5bbe40cade3de5c71e9e9b7"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
