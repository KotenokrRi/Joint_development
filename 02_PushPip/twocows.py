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