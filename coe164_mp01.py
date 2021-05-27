def get_c(data):
    v = int(data[0])
    m = str(data[1])
    n = int(data[2])
    c_table = {'L': [7, 10], 'M': [10, 16], 'Q': [13, 22], 'H': [17, 28]}
    c = c_table[m][v-1]
    return {'V': v, 'M': m, 'N': n, 'c': c}


def generate_alpha(i, alpha, a_list):
    if i == 256:
        return
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


def polynomial_generator(a_list, c):
    g = [0, 0]
    for i in range(1, c, 1):
        gb = []
        for j in g:
            gb.append((j + i) % 255)
        g.append(0)
        for k in range(len(gb)-1, -1, -1):
            g[k] = a_list.index(a_list[gb[k]]^a_list[g[k-1]])
        g[0] = gb[0]
    g.reverse()
    return g


def long_division(mx, a_list, gx, c, n):
    rx = mx.split(' ')
    rx = [int(i) for i in rx]
    for i in range(c):
        rx.append(0)
    for i in range(n-1):
        gx.append(0)
    while len(rx) > c:
        h = rx[0]
        if h == 0:
            del rx[0]
            del gx[-1]
            continue
        gh = gx.copy()
        for i in range(c+1):
            gh[i] = a_list[(gh[i] + a_list.index(h))%255]
        for i in range(c+1):
            rx[i] = gh[i]^rx[i]
    return rx


if __name__ == '__main__':
    T = input()
    lines = []
    for i in range(int(T)*2):
        lines.append(input())
    lines = [i.replace('\n', '') for i in lines]
    alpha_list = []
    msg_list = []
    data = []
    for i in range(0, len(lines), 1):
        if 2 < len(lines[i]) < 8:
            vmn = lines[i].split(' ')
            data.append(get_c(vmn))
            continue
        msg_list.append(lines[i])
    generate_alpha(0, 0, alpha_list)
    for i in range(len(msg_list)):
        temp = long_division(msg_list[i], alpha_list, polynomial_generator(alpha_list, data[i]['c']), data[i]['c'], data[i]['N'])
        final = ' '.join(map(str, temp))
        print(final)
