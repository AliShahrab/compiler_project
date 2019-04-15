import re

input_file = open("inp.txt", "r")

KEYWORD = ["if",
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

SYMBOL = [',',
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

WHITESPACE = [chr(32),
              chr(10),
              chr(11),
              chr(12),
              chr(13),
              chr(9)]


def get_next_token(inp, i=0):
    aux = ""
    if i >= len(inp) or inp[i] is '\n':
        return 0, 0, 0

    while True:
        if inp[i] in SYMBOL:
            if aux == "":
                return inp[i], "SYMBOL", i + 1
            else:
                return aux, category_aux, i
        elif inp[i] in WHITESPACE:
            if aux == "":
                return inp[i], "WHITESPACE", i + 1
            else:
                return aux, category_aux, i + 1

        aux += inp[i]
        category_aux = set_token_category(aux)

        if category_aux == "KEYWORD" and ((inp[i + 1] in WHITESPACE) or (inp[i + 1] in SYMBOL)):
            return aux, category_aux, i + 1

        elif category_aux is None:
            return aux, category_aux, i + 1

        i += 1


def set_token_category(token):

    category = None
    if re.match("^[0-9]+$", token):
        category = "NUM"

    elif token in KEYWORD:
        category = "KEYWORD"

    elif token in SYMBOL:
        category = "SYMBOL"

    elif token == "//":
        category = "cmt//"

    elif token == "/*":
        category = "cmt/*"

    elif token in WHITESPACE:
        category = "WHITESPACE"

    elif re.match("^[A-Za-z][A-Za-z0-9]*$", token):
        category = "ID"

    return category
#
# print(set_token_category("92342348"))
# print(set_token_category(";"))
# print(set_token_category("sdSSSD2"))
# print(set_token_category("@#$"))
# print(set_token_category("//"))
# print(set_token_category("/*"))
# print(set_token_category("else"))
# print(set_token_category(" "))

while True:

    inp_str = input_file.readline()
    i = 0
    while True:
        token, token_category, i = get_next_token(inp_str, i)
        if token == token_category == i == 0:
            break
        print(token, token_category, i)
    if inp_str is "":
        break
