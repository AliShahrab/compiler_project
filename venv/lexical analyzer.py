import re


class Compiler:
    def __init__(self):
        self.input_file = ''
        self.input = ''
        self.index = 0
        self.number_of_line = 1
        self.all_token = []
        self.INDEX_OF_CATEGORY = 0
        self.INDEX_OF_TOKEN = 1
        self.INDEX_OF_NUMBER_OF_LINE = 2
        self.all_error = []

        self.KEYWORD = ["if",
               "else",
               "void",
               "int",
               "while",
               "break",
               "continue",
               "switch",
               "default",
               "case",
               "return"]

        self.SYMBOL = [',',
              ':',
              ';',
              '{',
              '}',
              '(',
              ')',
              '[',
              ']',
              '+',
              '-',
              '*',
              '<',
              '=',
              '==']

        self.WHITESPACE = [chr(32),
                  chr(10),
                  chr(11),
                  chr(12),
                  chr(13),
                  chr(9)]

    def open_file(self, input_file):
        self.input_file = open(input_file, "r")
        # print(self.input)

    def get_next_token(self):
        aux = ""
        if self.index >= len(self.input):
            return 0, 0, 0, self.number_of_line
        while self.basic_check() and ((self.cheack_current_char() in self.WHITESPACE) or (self.cheack_current_char() == '/')):
            aux += self.read_current_char()
            if aux == '/':
                if self.cheack_current_char() == '/':
                    while  self.basic_check() and self.cheack_current_char() != '\n':
                        aux += self.read_current_char()
                    aux = ''
                    if not self.basic_check():
                        return 0, 0, 0, self.number_of_line
                    self.read_current_char()

                elif self.cheack_current_char() == '*':
                    while self.basic_check() and\
                            (not(self.basic_check() and (aux[len(aux) - 1] == '*') and (self.cheack_current_char() == '/'))):
                        aux += self.read_current_char()
                    aux = ''
                    if not self.basic_check():
                        return 0, 0, 0, self.number_of_line
                    self.read_current_char()
                else:
                    return self.set_error(aux)
            else:
                while self.basic_check() and self.cheack_current_char() in self.WHITESPACE:
                    self.read_current_char()
                aux = ''


        if re.match("^[0-9]+$", self.cheack_current_char()):
            while  self.basic_check() and (re.match("^[0-9]+$", self.cheack_current_char())):
                aux += self.read_current_char()
                # print('yess')
        elif re.match("^[A-Za-z]*$", self.cheack_current_char()):
            aux += self.read_current_char()
            while  self.basic_check() and (re.match("^[A-Za-z0-9]+$", self.cheack_current_char())):
                aux += self.read_current_char()
                # print(aux)
        elif self.cheack_current_char() in self.SYMBOL:
            if self.cheack_current_char() != '=':
                aux += self.read_current_char()
                return aux, self.set_token_category(aux), self.index, self.number_of_line
            else:
                aux += self.read_current_char()
                if self.cheack_current_char() == '=':
                    aux += self.read_current_char()
                    return aux, self.set_token_category(aux), self.index, self.number_of_line
                elif self.is_invalid_char(self.cheack_current_char()):
                    return self.set_error(aux), self.number_of_line
                else:
                    return aux, self.set_token_category(aux), self.index, self.number_of_line


        if self.basic_check() and self.is_invalid_char(self.cheack_current_char()):
            return self.set_error(aux)
        else:
            return aux, self.set_token_category(aux), self.index, self.number_of_line


            # if self.input[self.index] in self.SYMBOL:
            #     if aux == "":
            #         return self.input[self.index], "SYMBOL", self.index + 1
            #     else:
            #         return aux, category_aux, self.index
            # elif self.input[self.index] in self.WHITESPACE:
            #     if aux == "":
            #         return self.input[self.index], "WHITESPACE", self.index + 1
            #     else:
            #         return aux, category_aux, self.index + 1
            #
            # aux += self.input[self.index]
            # category_aux = self.set_token_category(aux)
            #
            # if category_aux == "KEYWORD" and ((self.input[self.index + 1] in self.WHITESPACE) or (self.input[self.index + 1] in self.SYMBOL)):
            #     return aux, category_aux, self.index + 1
            #
            # elif category_aux is None:
            #     return aux, category_aux, self.index + 1
            #
            # self.index += 1

    def set_error(self, aux):
        aux += self.read_current_char()
        return aux, 'ERROR', self.index, self.number_of_line

    def current_char_is_starter_for_parse(self, char):
        return (char in self.SYMBOL) or (re.match("^[A-Za-z0-9]*$"), char)

    def basic_check(self):
        return self.index < len(self.input)
    def read_current_char(self):
        self.index += 1
        if self.input[self.index - 1] == '\n':
            self.number_of_line += 1
        return self.input[self.index - 1]

    def cheack_current_char(self):
        if not self.basic_check():
            return
        return self.input[self.index]
    def is_invalid_char(self, char):
        # print('**' + char + '**')
        return not((char in self.SYMBOL) or (re.match("^[A-Za-z0-9]*$", char)) or (char in self.WHITESPACE) or (char is '/'))

    def set_token_category(self, token):

        category = None
        if re.match("^[0-9]+$", token):
            category = "NUM"

        elif token in self.KEYWORD:
            category = "KEYWORD"

        elif token in self.SYMBOL:
            category = "SYMBOL"

        elif token == "//":
            category = "cmt//"

        elif token == "/*":
            category = "cmt/*"

        elif token in self.WHITESPACE:
            category = "WHITESPACE"

        elif re.match("^[A-Za-z][A-Za-z0-9]*$", token):
            category = "ID"

        return category

    def process(self):

        self.input = self.input_file.read()
        # self.input = '!void!(main) !{start /end);== \n' \
        #              'asdf 123 wr asdf2 12d'
        print(self.input)
        self.index = 0
        number_if_line = 0
        while True:
            token, token_category, self.index, number_if_line = self.get_next_token()
            if token == token_category == self.index == 0:
                break
            if token_category != 'ERROR':
                self.all_token.append([token_category, token, number_if_line])
            else:
                self.all_error.append([token_category, token, number_if_line])
            # print(token, token_category, self.index)

    def show_tokens(self):
        counter = 0
        for i in range(self.number_of_line):
            j = i + 1
            if counter < len(self.all_token) and j == self.all_token[counter][self.INDEX_OF_NUMBER_OF_LINE]:
                print(str(j) + '. ', end='')
                while counter < len(self.all_token) and j == self.all_token[counter][self.INDEX_OF_NUMBER_OF_LINE]:
                    print('(' + str(self.all_token[counter][self.INDEX_OF_CATEGORY]) + ', ' +
                          str(self.all_token[counter][self.INDEX_OF_TOKEN]) + ')', end='')
                    counter += 1
                print()

    def show_error(self):
        counter = 0
        print(self.all_error)
        for i in range(self.number_of_line):
            j = i + 1
            if counter < len(self.all_error) and j == self.all_error[counter][self.INDEX_OF_NUMBER_OF_LINE]:
                print(str(j) + '. ', end='')
                while counter < len(self.all_error) and j == self.all_error[counter][self.INDEX_OF_NUMBER_OF_LINE]:
                    print('(' + str(self.all_error[counter][self.INDEX_OF_CATEGORY]) + ', ' +
                          str(self.all_error[counter][self.INDEX_OF_TOKEN]) + ')', end='')
                    counter += 1
                print()


my_comiler = Compiler()
my_comiler.open_file('inp.txt')

my_comiler.process()
my_comiler.show_tokens()
my_comiler.show_error()


#
# print(set_token_category("92342348"))
# print(set_token_category(";"))
# print(set_token_category("sdSSSD2"))
# print(set_token_category("@#$"))
# print(set_token_category("//"))
# print(set_token_category("/*"))
# print(set_token_category("else"))
# print(set_token_category(" "))

