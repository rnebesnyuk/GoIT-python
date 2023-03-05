from datetime import datetime
import logging

def factorize(*number):
    division_list = []
    for el in number:
        division_list.append([_ for _ in range (1, el + 1) if not el % _])
    return division_list


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    current_t = datetime.now()
    a, b, c, d  = factorize(128_567_980, 255, 99999, 104_651_060)
    delta_t = datetime.now() - current_t
    logging.info(f'{delta_t}')

    # assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    # assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    # assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    # assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]