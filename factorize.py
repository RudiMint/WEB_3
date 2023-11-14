from datetime import datetime


def factorize(*numbers):
    start_time = datetime.now()
    dividers_list = []
    for number in numbers:
        dividers_list_for = []
        num = 1
        while num <= number:
            if number % num == 0:
                dividers_list_for.append(num)
            num += 1
        dividers_list.append(dividers_list_for)

    print(datetime.now() - start_time)
    return dividers_list


if __name__ == "__main__":
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    print(a, b, c, d)
