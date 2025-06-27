import random
import sys
import urllib.request
import cowsay
def bullscows(guess: str, secret: str) -> tuple[int, int]:
    """
    Сравнивает догадку и загаданное слово, возвращает количество 'быков' и 'коров'.
    Пример: bullscows("потоп", "полип") -> (1, 1) # 'п' - бык, 'о' - корова
    """
    bulls = 0
    cows = 0

    # Чтобы не считать одну и ту же букву дважды
    secret_list = list(secret)
    guess_list = list(guess)

    # Сначала ищем быков (самое важное!)
    for i in range(len(guess_list)):
        if guess_list[i] == secret_list[i]:
            bulls += 1
            # "Вычеркиваем" найденного быка
            guess_list[i] = None
            secret_list[i] = None

    # Теперь ищем коров
    for i in range(len(guess_list)):
        if guess_list[i] is not None and guess_list[i] in secret_list:
            cows += 1
            # удаляем коровку
            secret_list.remove(guess_list[i])

    return bulls, cows


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    """
    Основной игровой цикл.
    - ask: функция для запроса ввода у пользователя.
    - inform: функция для вывода информации пользователю.
    - words: список слов для загадывания.
    """
    secret = random.choice(words)
    attempts = 0

    while True:
        attempts += 1
        guess = ask("Введите слово: ", words)

        bulls, cows = bullscows(guess, secret)

        inform("Быки: {}, Коровы: {}", bulls, cows)

        if bulls == len(secret):
            print(f"Вы угадали! Загаданное слово: {secret}. Попыток: {attempts}")
            return attempts

if __name__ == "__main__":
    # 1. Получаем аргументы из командной строки
    try:
        dictionary_path = sys.argv[1]
        word_length = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    except IndexError:
        print("Ошибка: Укажите путь к словарю и, опционально, длину слова.")
        print("Пример: python -m bullscows russian_nouns.txt 5")
        sys.exit(1)

    # 2. Загружаем и фильтруем слова
    try:
        if dictionary_path.startswith("http"):
            with urllib.request.urlopen(dictionary_path) as response:
                word_list = response.read().decode('utf-8').splitlines()
        else:
            with open(dictionary_path, 'r', encoding='utf-8') as f:
                word_list = f.read().splitlines()
    except Exception as e:
        print(f"Ошибка при загрузке словаря: {e}")
        sys.exit(1)

    # Фильтруем слова по длине
    valid_words = [word for word in word_list if len(word) == word_length]

    if not valid_words:
        print(f"В словаре нет слов длиной {word_length}.")
        sys.exit(1)

    # 3. Определяем простые функции ask и inform для консоли
    def ask_cli(prompt: str, valid: list[str] = None):
        while True:
            user_input = input(prompt)
            if valid and user_input not in valid:
                print("Такого слова нет в словаре или его длина неверна.")
                continue
            return user_input


    my_robot = """
     $thoughts
      $thoughts
         [__]
         (oo)
        /|__|\\
       / |  | \\
      /  |  |  \\
     |   |  |   |
     |   |  |   |
     '---'--'---'
    """


    def inform_cli_cowsay(format_string: str, bulls: int, cows: int):
        message = format_string.format(bulls, cows)
        # Используем нашего робота в параметре cow
        print(cowsay.cowsay(message, cow=my_robot))


    # Запускаем игру с новой функцией
    gameplay(ask=ask_cli, inform=inform_cli_cowsay, words=valid_words)