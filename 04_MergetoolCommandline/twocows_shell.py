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

if __name__ == '__main__':
    TwoCowsShell().cmdloop()