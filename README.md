# 2D Barcode Error-Correcting Program

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

## 🚀 Quickstart

### 1. Programming Language

- Programming language used is **Python** with the intention of having less code.

### 2. Operations

- Generates a list of a^n
- Obtains a list of g(x)
- Computes for the list of codewords using long division

### 3. Running the program

- The usual

    ```bash
    $ python3 main.py
    ```

- Input redirection

    ```bash
    $ python3 main.py < input.txt
    ```

- Input and output redirection

    ```bash
    $ python3 main.py < input.txt > output.txt
    ```

### 4. Author

- Joie Angelo Llantero

# 🧮 Program Algorithms

A discussion on the algorithms used in this program.

### 1. Input Handling

The user may use the terminal to input the necessary details for the program or opt to do an input redirection and feed a text file containing the necessary details.

Shown below is how the latter should be done.

```bash
$ python3 main.py < in_[date]_[time].txt
```

The algorithm I implemented was pretty straightforward—using a single for loop. The first input or the first line in the text file is the number of messages, T. I double this value since each messages have two lines, i.e., the line containing the values of V, M, and N and the message itself.  Afterwards, I loop through all the inputs and save them in an array. The loop stops when it reaches the value of T*2.

The code snippet for the input handling algorithm is shown below.

```python
T = input()
lines = []
for i in range(int(T)*2):
    lines.append(input())
```

Moreover, I used another for loop to store the values of V, M, and N in a dictionary and the message in a list for later use in the program, e.g., obtaining the value of c.

### 2. Generating the Alpha List

The alpha generator function makes use of recursion. This algorithm was chosen because it gave better code readability while still having a straightforward solution.

In the `generate_alpha` function, it takes in three arguments, i.e., `i`, `alpha`, and `a_list`. `i` is the iteration variable, `alpha` is the calculated alpha value, and `a_list` contains the stored alpha values.

When the function is called, it checks several conditions but when $i < 8$, it computes for the alpha by solving `2**i`. However, when $i ≥ 8$, it computes for the alpha by multiplying it by 2 and checking if the alpha value is greater than 256. If it is greater than 256, it should do an XOR operation by 285. Finally, when the iteration variable, `i`, reaches 256, it should end the loop and return to the main function. By then, the `alpha_list` list variable declared in the main function is already updated. This will be used in the later steps.

Below is the code for the function, `generate_alpha`.

```python
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
```

### 3. Obtaining $g(x)$

Using the generated alpha list and the value of c, we can now compute for g(x). In this part of the program, it should generate a list containing the computed values of g(x).

The algorithm used is a nested for loop. There are two for loops insides the main for loop which has a range from 1 to c. A new empty list is declared at the beginning of the main loop as this is a temporary variable where we store the calculated values.

Shown below is the code snippet for the `polynomial_generator` function.

```python
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
```

Notice the initialization of list variable g is [0, 0] because this is simpler than initializing it like this `g = [0]` and doing `g.append(0)`.

Discussing the algorithm further, we take the first loop inside the main for loop, i.e.,

```python
for j in g:
    gb.append((j + i) % 255)
```

This loop simply adds the current value of the iteration variable to an element in list g then we mod it with 255 since we wan the result to be within the index of the alpha list. Afterwards, we store the result in a temporary list variable, gb.

Now, we discuss the second for loop, i.e.,

```python
for k in range(len(gb)-1, -1, -1):
            g[k] = a_list.index(a_list[gb[k]]^a_list[g[k-1]])
```

The above code snippet continues the calculation of the values of g(x). First, we convert the message into its antilog form, i.e., `a_list[gb[k]` and `a_list[g[k-1]]`. Afterwards, we do an XOR operation to convert it back to log.

Before we return the value, we use the `reverse()` method to "unreverse" the result and get the correct arrangement or pattern.

### 4. Computing for Long Division

The algorithm used for this part of the program uses nested loops. Shown below is the code snippet for the `long_division` function

```python
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
```

First, we take the message that was saved earlier, and turn that into a list. Afterwards, we convert all the elements into integers as we will be using these values in mathematical operations later.

Next, we have two for loops which will add zeroes to list `rx` and list `gx` so that they will have equal length. This will avoid in getting an index error later on. Also, remember that list `gx` is the value returned from the function `polynomial_generator`.

Moving on to the `while` loop, we go through the loop as long as the length of `rx` is greater than `c`. We first initialize the temporary variable h as the first element in list `rx` then we check if h is equal to zero. If it is, we delete the first element in list `rx` and the last element in list `gx`. Once this was done, we will skip the lines below, i.e., below `continue`, and begin at the top of the loop again. On the contrary, if h ≠ 0, then we copy the value of `gx` to a temporary list variable `gh`.

Now, we have two for loops. The first one (seen below) is to compute for addition of every term in g to the antilog of h then we mod the sum with 255 to avoid index error.

```python
for i in range(c+1):
    gh[i] = a_list[(gh[i] + a_list.index(h))%255]
```

On the other hand, the second one (seen below) is to obtain the XOR of the elements in `gh` and `rx`.

```python
for i in range(c+1):
    rx[i] = gh[i]^rx[i]
```

When the computation is done, we return the value of `rx`.

## 👨‍💻 Author

- [Joie Llantero](https://github.com/joiellantero)


## 📄 License 

- [MIT license](http://opensource.org/licenses/mit-license.php)
