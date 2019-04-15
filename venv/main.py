class Compiler:
    def __init__(self):
        self.in_text = ''
        self.output = []
        self.pointer = 0

    def set_in_text(self, text):
        self.in_text = text

    def next_elment(self):
        self.pointer += 1
        return self.in_text[self.pointer]

