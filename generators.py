

def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def main():
    # Печатает все числа последовательности Фибоначчи, меньше 1000
    for i in fibonacci_generator():
        if i > 10:
            break
        print(i)

if __name__ == "__main__":
    main()