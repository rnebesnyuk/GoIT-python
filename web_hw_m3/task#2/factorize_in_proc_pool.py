from multiprocessing import Pool, current_process, cpu_count
from datetime import datetime
import logging


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def factorize(number):
    logging.info(f"pid={current_process().pid}, number={number}")
    division_list = []
    for num in range (1, number + 1):
        if not number % num:
            division_list.append(num)
    return division_list

if __name__ == '__main__':
    data  = (128_567_980, 255, 99999, 104_651_060)
    current_t = datetime.now()
    with Pool(processes=cpu_count()) as pool:
        result = pool.map_async(factorize, data)
        logging.info(result.get())
    delta_t = datetime.now() - current_t
    logging.info(f'{delta_t}')
