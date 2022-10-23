

class StringBuffer:
    lines = None
    index = -1
    length = -1

    def __init__(self, lines: str):
        self.lines = lines
        self.index = 0
        self.length = len(lines)

    def getline(self):
        index = self.index
        self.index += 1
        return self.lines[index]

    def ungetline(self):
        self.index = max(0, self.index - 1)

    def reading(self):
        return self.index != self.length