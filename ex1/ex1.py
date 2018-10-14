from sys import exit


def parse_args():
    try:
        begin = int(input())
        end = int(input())
    except ValueError:
        print('The argument you entered is invalid. Use only integers between 1 and 10000')
        exit(1)
    else:
        if 1 <= begin < end <= 10000:
            return begin, end
        else:
            print('The input does not satisfy requirements. Use numbers between 1 and 10000, with the second argument '
                  'bigger than the first one. ')
            exit(1)


def fizzbuzz():
    begin, end = parse_args()
    for num in range(begin, end+1):
        if num % 15 == 0:
            print('Fizzbuzz')
        elif num % 3 == 0:
            print('Fizz')
        elif num % 5 == 0:
            print('Buzz')
        else:
            print(num)


if __name__ == '__main__':
    fizzbuzz()
