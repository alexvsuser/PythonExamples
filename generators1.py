def countdown(n):
    print('Обратный отсчет!')
    while n > 0:
        yield n  # Генерирует значение (n)
        n -= 1


def main():
    # for i in countdown(5):
    #     print(i)
    cd = countdown(5)
    while True:
        try:
            print(cd.__next__())
        except StopIteration:
            cd.close()
            raise StopIteration('Окончание итерации!')

            break


if __name__ == "__main__":
    main()