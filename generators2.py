# следит за содержимым файла (аналог команды tail -f)
import time


def tail(f):
    f.seek(0, 2)
    # Переход в конец файла
    while True:
        try:
            line = f.readline()  # Попытаться прочитать новую строку текста
            if not line:
                # Если ничего не прочитано,
                time.sleep(0.1)  # приостановиться на короткое время
                continue  # и повторить попытку
            yield line
        except KeyboardInterrupt:
            print('Прерывание от клавиутуры')


def grep(lines, searchtext):
    for line in lines:
        if searchtext in line:
            yield line


def print_matches(matchtext):
    print('Поиск подстроки', matchtext)
    while True:
        line = (yield)  # Получение текстовой строки
        if matchtext in line:
            print('Нашел подстроку: ' + matchtext + ', вот! ')
            print(line)


def main():
    # with open('/var/log/syslog', 'r') as f:
    #     syslog = tail(f)
    #     greplog = grep(syslog, 'transaction')
    #     for s in greplog:
    #         print(s)

    # Множество сопрограмм поиска
    matchers = [print_matches('Updating'), print_matches('Processing transaction'),
                print_matches('Finished transaction'), print_matches('Simulating trans'),
                print_matches('Queuing transaction'), print_matches('CMD'), print_matches('CRON'),
                print_matches('org.debian.apt')
                ]

    # Подготовка всех подпрограмм к последующему вызову метода next()
    for m in matchers:
        m.__next__()

    with open('/var/log/syslog', 'r') as f:
        syslog = tail(f)
        for line in syslog:
            for m in matchers:
                m.send(line)  # Передача данных каждой из сопрограмм


if __name__ == '__main__':
    main()
