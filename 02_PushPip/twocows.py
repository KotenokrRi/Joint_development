import argparse
import cowsay
import sys

def main():
    #Парсинг аргументов
    parser = argparse.ArgumentParser(
        description="A program that displays two talking characters, similar to cowsay."
    )

    parser.add_argument('-e', '--eye_string', default='oo', help='Selects the appearance of the cow\'s eyes.')
    parser.add_argument('-f', '--cowfile', default='default', help='Specifies a particular cow picture file to use.')
    parser.add_argument('-T', '--tongue_string', default='  ', help='Selects the appearance of the cow\'s tongue.')
    parser.add_argument('-W', '--width', type=int, default=40, help='Specifies the width of the message bubble.')

    parser.add_argument('-E', '--eye_string2', help='Selects the appearance of the second cow\'s eyes.')
    parser.add_argument('-F', '--cowfile2', help='Specifies a particular cow picture file for the second cow.')
    parser.add_argument('-T2', '--tongue_string2', help='Selects the appearance of the second cow\'s tongue.')

    parser.add_argument('message', nargs='*', help='The messages for the characters to say.')

    args = parser.parse_args()

    if not args.message:
        print("Available cowfiles:")
        print(' '.join(cowsay.list_cows()))
        sys.exit(0)

    message1 = args.message[0]
    message2 = args.message[1] if len(args.message) > 1 else ""

    # Генерация изображений (здесь финальные исправления)
    cow1_output = cowsay.cowsay(
        message=message1,
        cow=args.cowfile,
        eyes=args.eye_string,
        tongue=args.tongue_string,
        width=args.width
    )

    cow2_output = cowsay.cowsay(
        message=message2,
        cow=args.cowfile2 if args.cowfile2 else 'default',
        eyes=args.eye_string2 if args.eye_string2 else args.eye_string,
        tongue=args.tongue_string2 if args.tongue_string2 else args.tongue_string,
        width=args.width
    )

    # Объединение и вывод (не меняется)
    lines1 = cow1_output.split('\n')
    lines2 = cow2_output.split('\n')

    max_lines = max(len(lines1), len(lines2))

    while len(lines1) < max_lines:
        lines1.insert(0, '')
    while len(lines2) < max_lines:
        lines2.insert(0, '')

    # Находим максимальную ширину для корректного отступа
    max_width1 = 0
    if lines1:  # Проверка на случай, если вывод пустой(
        max_width1 = max(len(line) for line in lines1)

    final_output = []
    for i in range(max_lines):
        combined_line = lines1[i].ljust(max_width1) + " " + lines2[i]
        final_output.append(combined_line)

    print('\n'.join(final_output))


if __name__ == '__main__':
    main()