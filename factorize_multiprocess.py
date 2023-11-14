from datetime import datetime
from multiprocessing import Pool, cpu_count


def factorize(*numbers):
    dividers_list = []
    for number in numbers:
        dividers_list_for = []
        num = 1
        while num <= number:
            if number % num == 0:
                dividers_list_for.append(num)
            num += 1
        dividers_list.append(dividers_list_for)

    return dividers_list


if __name__ == "__main__":
    start_time = datetime.now()
    with Pool(cpu_count()) as pool:
        results = pool.map(factorize, [128, 255, 99999, 10651060])
        pool.close()
    a, b, c, d = results
    print(datetime.now() - start_time)
    print(a, b, c, d)

