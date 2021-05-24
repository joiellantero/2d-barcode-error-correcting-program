def get_c(data):
    v = int(data[0])
    m = str(data[1])
    n = int(data[2])
    c_table = {'L': [7, 10], 'M': [10, 16], 'Q': [13, 22], 'H': [17, 28]}
    c = c_table[m][v-1]
    return {'V': v, 'M': m, 'N': n, 'c': c}


def generate_alpha(i, alpha, a_list):
    if i == 256:
        return alpha

    elif i < 8:
        alpha = 2**i
        a_list.append(alpha)
        return generate_alpha(i+1, alpha, a_list)

    elif i >= 8:
        alpha *= 2
        if alpha >= 256:
            alpha = alpha ^ 285
        a_list.append(alpha)
        return generate_alpha(i+1, alpha, a_list)


if __name__ == '__main__':
    with open('testcase.txt') as f:
        lines = f.readlines()
        lines = [i.replace('\n', '') for i in lines]
        alpha_list = []
        for line in lines:
            if 2 < len(line) < 8:
                vmn = line.split(' ')
                data = get_c(vmn)
                print('c:', data['c'])
                continue
            print('codewords: ', line)
        a = generate_alpha(0, 0, alpha_list)
        print('alpha list:', alpha_list)