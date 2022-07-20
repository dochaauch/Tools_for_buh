def create_toler_list(digit, toler):
    '''
    :param digit: число из списка, например 5.44
    :param toler: количество значений допуска по 0.01 в каждую сторону, например 2
    :return: список 5.42, 5.43, 5.44, 5.45, 5.46
    '''
    l_ = [digit]
    num_m, num_p = digit, digit
    for i in range(toler):
        num_p += 0.01
        num_m -= 0.01
        l_.append(round(num_p, 2))
        l_.append(round(num_m, 2))
    return sorted(l_)


def find_s_k_lists(i, km_rate):
    s = round(i / (1 + km_rate), 2)
    k = round(s * km_rate, 2)
    list_s = create_toler_list(s, 2)
    list_k = create_toler_list(k, 2)
    print(s, k, list_s, list_k, km_rate)
    return s, k, list_s, list_k


def find_total_sum_km(all_digits, km_rate_list):
    print('нормальный перебор', all_digits)
    for i in all_digits:
        for km_rate in km_rate_list:
            s, k, list_s, list_k = find_s_k_lists(i, km_rate)
            if any(s_ in list_s for s_ in all_digits) and any(k_ in list_k for k_ in all_digits) and i != 0.0 \
                    and i > 0.5:
                total_sum = i
                arve_sum = [s_ for s_ in all_digits if s_ in list_s][0]
                arve_km = [k_ for k_ in all_digits if k_ in list_k][0]
                print(arve_sum, 'внутри списка', arve_km)
                print('here', total_sum)
                flag_total = True
                return total_sum, arve_sum, arve_km
    return 0.0, 0.0, 0.0


def find_km_no_sum(all_digits, km_rate_list):
    print('ищем налог без суммы', all_digits)
    for i in all_digits:
        for km_rate in km_rate_list:
            # если налог находит, но не находит сумму без налога
            s, k, list_s, list_k = find_s_k_lists(i, km_rate)
            if i != 0.0 and i > 1 and any(k_ in list_k for k_ in all_digits):
                total_sum = i
                arve_km = [k_ for k_ in all_digits if k_ in list_k][0]
                print('вариант с налогом', total_sum, arve_km)
                if arve_km + s == i:
                    arve_sum = s
                else:
                    arve_sum = i - arve_km
                return total_sum, arve_sum, arve_km
    return 0.0, 0.0, 0.0


def find_sum_no_km(all_digits, km_rate_list):
    print('ищем сумму без налога', all_digits)
    for i in all_digits:
        for km_rate in km_rate_list:
            # если сумму находит, но не находит налог
            s, k, list_s, list_k = find_s_k_lists(i, km_rate)
            if i != 0.0 and i > 1 and any(s_ in list_s for s_ in all_digits):
                total_sum = i
                arve_sum = [s_ for s_ in all_digits if s_ in list_s][0]
                print('вариант суммы, но нет налога', total_sum, arve_sum)
                if arve_sum + k == i:
                    arve_km = k
                else:
                    arve_km = i - arve_sum
                return total_sum, arve_sum, arve_km
    return 0.0, 0.0, 0.0


def take_only_total(all_digits):
    return all_digits[0]

