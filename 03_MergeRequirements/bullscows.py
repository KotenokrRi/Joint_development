import random
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