import re


class Compiler:
    def __init__(self):
        self.input_file = ''
        self.input = ''
        self.index = 0

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

    def get_next_token(self,):
        aux = ""
        if self.index >= len(self.input) or self.input[self.index] is '\n':
            return 0, 0, 0

        while True:
            if self.input[self.index] in self.SYMBOL:
                if aux == "":
                    return self.input[self.index], "SYMBOL", self.index + 1
                else:
                    return aux, category_aux, self.index
            elif self.input[self.index] in self.WHITESPACE:
                if aux == "":
                    return self.input[self.index], "WHITESPACE", self.index + 1
                else:
                    return aux, category_aux, self.index + 1

            aux += self.input[self.index]
            category_aux = self.set_token_category(aux)

            if category_aux == "KEYWORD" and ((self.input[self.index + 1] in self.WHITESPACE) or (self.input[self.index + 1] in self.SYMBOL)):
                return aux, category_aux, self.index + 1

            elif category_aux is None:
                return aux, category_aux, self.index + 1

            self.index += 1


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
        while True:

            self.input = self.input_file.readline()
            self.index = 0
            while True:
                token, token_category, self.index = self.get_next_token()
                if token == token_category == self.index == 0:
                    break
                print(token, token_category, self.index)
            if self.input is "":
                break


my_comiler = Compiler()
my_comiler.open_file('inp.txt')
my_comiler.process()




#
# print(set_token_category("92342348"))
# print(set_token_category(";"))
# print(set_token_category("sdSSSD2"))
# print(set_token_category("@#$"))
# print(set_token_category("//"))
# print(set_token_category("/*"))
# print(set_token_category("else"))
# print(set_token_category(" "))

