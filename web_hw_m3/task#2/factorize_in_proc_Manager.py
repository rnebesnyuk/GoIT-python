from datetime import datetime
import logging
from multiprocessing import Process, Manager, current_process



def factorize(number, val):
    name = current_process().name
    division_list = []
    for num in range (1, number + 1):
        if not number % num:
            division_list.append(num)
    val[name] = current_process().pid
    logging.info(f'Done: {name}')
    return division_list


    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(processName)s %(message)s')
    current_t = datetime.now()
    with Manager() as manager:
        m = manager.dict()
        a, b, c, d = (128_567_980, 255, 99999, 104_651_060)
        processes = []
        for num in a, b, c, d:
            pr = Process(target=factorize, args=(num, m))
            pr.start()
            processes.append(pr)
            
        [pr.join() for pr in processes]
        print(m)
    delta_t = datetime.now() - current_t
    logging.info(f'{delta_t}')
