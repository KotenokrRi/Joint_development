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

if __name__ == '__main__':
    TwoCowsShell().cmdloop()