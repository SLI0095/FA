from PIL import Image

MAX_COLOR = 255
MAX_BIT = 8


def remove_n_lsb(value, n):
    value = value >> n
    return value << n


def get_n_lsb(value, n):
    value = value << MAX_BIT - n
    value = value % MAX_COLOR
    return value >> MAX_BIT - n


def get_n_msb(value, n):
    return value >> MAX_BIT - n


def n_bits_to_8(value, n):
    return value << MAX_BIT - n


def create_image(data, resolution):
    image = Image.new("RGB", resolution)
    image.putdata(data)
    return image


def encode(source, secret_image, n):
    width, height = source.size
    secret_image = secret_image.load()
    hiding_image = source.load()
    data = []

    for y in range(height):
        for x in range(width):
            try:
                secret_r, secret_g, secret_b = secret_image[x, y]
                hide_r, hide_g, hide_b = hiding_image[x, y]

                secret_r = get_n_msb(secret_r, n)
                secret_g = get_n_msb(secret_g, n)
                secret_b = get_n_msb(secret_b, n)

                hide_r = remove_n_lsb(hide_r, n)
                hide_g = remove_n_lsb(hide_g, n)
                hide_b = remove_n_lsb(hide_b, n)

                data.append((secret_r + hide_r,
                             secret_g + hide_g,
                             secret_b + hide_b))

            except Exception as e:
                print(e)

    return create_image(data, source.size)


def decode(encoded, n):
    width, height = encoded.size
    encoded_image = encoded.load()
    data = []

    for y in range(height):
        for x in range(width):
            image_r, image_g, image_b = encoded_image[x, y]
            image_r = n_bits_to_8(get_n_lsb(image_r, n), n)
            image_g = n_bits_to_8(get_n_lsb(image_g, n), n)
            image_b = n_bits_to_8(get_n_lsb(image_b, n), n)

            data.append((image_r, image_g, image_b))

    return create_image(data, encoded.size)


if __name__ == '__main__':
    cmd = int(input("For encoding enter 1, for decoding enter 2: "))
    if cmd == 1:
        n = int(input("Enter number of hidden bits (max 7): "))
        while n > 7:
            n = int(input("Enter number of hidden bits (max 7): "))
        secret_path = input("Enter path to image you want to hide: ")
        cover_path = input("Enter path to cover image: ")
        result_path = input("Enter name for result (without extension): ") + ".png"
        secret = Image.open(secret_path)
        image_to_hide_in = Image.open(cover_path)
        secret = secret.resize(image_to_hide_in.size)
        encode(image_to_hide_in, secret, n).save(result_path)
    elif cmd == 2:
        n = int(input("Enter number of hidden bits (max 7): "))
        while n > 7:
            n = int(input("Enter number of hidden bits (max 7): "))
        decoding_path = input("Enter path to image to decode: ")
        result_path = input("Enter name for result (without extension): ") + ".png"
        decoding = Image.open(decoding_path)
        decode(decoding, n).save(result_path)
