from datetime import datetime
from threading import Thread
import logging


def factorize(number):
    division_list = []
    for num in range (1, number + 1):
        if not number % num:
            division_list.append(num)
    return division_list


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    threads = []
    current_t = datetime.now()
    a, b, c, d  = (128_567_980, 255, 99999, 104_651_060)
    for el in a,b, c, d:
        th = Thread(target=factorize, args=(el,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    delta_t = datetime.now() - current_t
    logging.info(f'{delta_t}')
    
