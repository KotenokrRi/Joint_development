import cmd
import shlex
import cowsay

class TwoCowsShell(cmd.Cmd):
    """
    Интерактивная оболочка для вывода двух говорящих персонажей.
    """
    intro = "Welcome to the Two Cows shell. Type help or ? to list commands.\n"
    prompt = "twocows> "

    def do_exit(self, args):
        """Exits the shell."""
        print("Thank you for using Two Cows shell!")
        return True

    def do_EOF(self, args):
        """Exits the shell on Ctrl+D."""
        return self.do_exit(args)

    def do_list_cows(self, args):
        """
        Lists all available cow character names that can be used with the cowsay command.
        """

        available_cows = cowsay.list_cows()

        print("Available cows:")
        print(' '.join(available_cows))

    def help_list_cows(self):
        """
        Prints the help message for the 'list_cows' command.
        """
        print("\nUsage: list_cows")
        print("Description: Lists all available cowfiles (character names) that can be used.")
        print("Example: ")
        print("twocows> list_cows\n")

    def print_two_cows(self, params1, params2):
        """Вспомогательная функция для отрисовки двух персонажей."""
        #Этот код практически полностью взят из ДЗ про двух коров
        message1 = params1.pop('message', '')
        message2 = params2.pop('message', '')

        # Передаем остальные параметры (cow, eyes, tongue) в функцию cowsay
        cow1_output = cowsay.cowsay(message=message1, **params1)
        cow2_output = cowsay.cowsay(message=message2, **params2)

        lines1 = cow1_output.split('\n')
        lines2 = cow2_output.split('\n')

        max_lines = max(len(lines1), len(lines2))

        while len(lines1) < max_lines: lines1.insert(0, '')
        while len(lines2) < max_lines: lines2.insert(0, '')

        # Добавляем +1 для пробела между картинками
        max_width1 = max(len(line) for line in lines1) + 1 if lines1 else 0

        for i in range(max_lines):
            print(lines1[i].ljust(max_width1) + lines2[i])

    def do_cowsay(self, args):
        """
        Displays one or two talking characters.
        """
        try:
            # Разбиваем строку аргументов на токены
            tokens = shlex.split(args)

            #Ищем 'reply', чтобы разделить аргументы для двух коров
            if 'reply' in tokens:
                reply_index = tokens.index('reply')
                tokens1 = tokens[:reply_index]
                tokens2 = tokens[reply_index + 1:]
            else:
                tokens1 = tokens
                tokens2 = []

            # Вложенная функция для парсинга аргументов одного персонажа
            def parse_cow_args(token_list):
                params = {'cow': 'default'}  # Значение по умолчанию
                positional_args = []
                for token in token_list:
                    if '=' in token:
                        key, value = token.split('=', 1)
                        # Проверяем, что это валидный параметр для cowsay
                        if key in ['eyes', 'tongue', 'width', 'cow']:
                            params[key] = value
                    else:
                        positional_args.append(token)

                # Первый позиционный аргумент - это сообщение
                if positional_args:
                    params['message'] = positional_args.pop(0)
                # Второй (если есть) - это имя персонажа
                if positional_args:
                    params['cow'] = positional_args.pop(0)

                return params

            # Парсим аргументы для каждой коровы
            params1 = parse_cow_args(tokens1)
            params2 = parse_cow_args(tokens2)

            # Вызываем функцию отрисовки
            self.print_two_cows(params1, params2)

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please check your syntax. Use 'help cowsay' for usage details.")

    def help_cowsay(self):
        """Prints the help message for the 'cowsay' command."""
        print("\nUsage: cowsay MESSAGE [COW] [PARAM=VALUE...]")
        print("       cowsay ... reply MESSAGE [COW] [PARAM=VALUE...]\n")
        print("Description: Displays one or two talking characters.")
        print("Parameters: eyes, tongue, width, cow.")
        print('Example: cowsay "Hello" moose eyes=^^ reply "World" sheep\n')

    def do_cowthink(self, args):
        """
        Displays one or two thinking characters.
        Syntax is identical to 'cowsay'. Use 'help cowsay' for details.
        """

        original_printer = self.print_two_cows
        self.print_two_cows = self.print_two_cows_thinking

        try:
            self.do_cowsay(args)  # Вызываем уже существующий do_cowsay с теми же аргументами
        finally:
            # Возвращаем все как было, чтобы не сломать обычный cowsay
            self.print_two_cows = original_printer

    def print_two_cows_thinking(self, params1, params2):
        """Вспомогательная функция для отрисовки думающих персонажей."""
        message1 = params1.pop('message', '')
        message2 = params2.pop('message', '')

        # Единственное отличие - вызываем cowthink вместо cowsay
        cow1_output = cowsay.cowthink(message=message1, **params1)
        cow2_output = cowsay.cowthink(message=message2, **params2)

        # Остальной код для вывода бок о бок точно такой же
        lines1 = cow1_output.split('\n')
        lines2 = cow2_output.split('\n')
        max_lines = max(len(lines1), len(lines2))

        while len(lines1) < max_lines: lines1.insert(0, '')
        while len(lines2) < max_lines: lines2.insert(0, '')

        max_width1 = max(len(line) for line in lines1) + 1 if lines1 else 0

        for i in range(max_lines):
            print(lines1[i].ljust(max_width1) + lines2[i])

    def help_cowthink(self):
        """Prints the help message for the 'cowthink' command."""
        print("\nDisplays one or two thinking characters.")
        print("The syntax is identical to the 'cowsay' command.")
        print("Please use 'help cowsay' for detailed usage instructions.\n")

    def do_make_bubble(self, args):
        """
        Creates a speech bubble with the given text.
        """
        # Здесь нам не нужен сложный парсер, т.к. все аргументы - это просто текст.
        # shlex.split поможет, если мы захотим передать параметры для bubble, но пока упростим.
        try:
            bubble_text = cowsay.make_bubble(text=args)
            print(bubble_text)
        except Exception as e:
            print(f"Error creating bubble: {e}")

    def help_make_bubble(self):
        """Prints the help message for the 'make_bubble' command."""
        print("\nUsage: make_bubble [TEXT]")
        print("Description: Wraps the given text in a speech bubble.\n")

if __name__ == '__main__':
    TwoCowsShell().cmdloop()