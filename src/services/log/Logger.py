import colorama


class Logger():

    divider_size = 45

    def __init__(self, log_context):
        colorama.init()
        self.log_context = log_context

    def info(self, message):
        print('{}[+] ({}){}: {}'.format(colorama.Fore.BLUE,
              self.log_context, colorama.Fore.RESET, message))

    def warn(self, message):
        print('{}[!] ({}){}: {}'.format(colorama.Fore.YELLOW,
              self.log_context, colorama.Fore.RESET, message))

    def error(self, message):
        print('{}[!] ({}){}: {}'.format(colorama.Fore.RED,
              self.log_context, colorama.Fore.RESET, message))

    def success(self, message):
        print('{}[+] ({}){}: {}'.format(colorama.Fore.GREEN,
              self.log_context, colorama.Fore.RESET, message))

    def divider(self):
        print('-' * self.divider_size)
