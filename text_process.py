import re

class LineHandler:
    def __init__(self, data, lastLineComplete) -> None:
        self.__line = data
        self.__lastLineComplete = lastLineComplete
        self.__last_tail = None
        self.__cut_sentence()
        self.__integrate()

    def __cut_sentence(self):
        self.__sentences = re.split(
            '\n', 
            re.sub('\.\s[0-9][a-zA-Z]', lambda matched: matched.group()[:2] + '\n' + matched.group()[-2:], 
                re.sub('\.\s[A-Z]', lambda matched: matched.group()[:2] + '\n' + matched.group()[-1], 
                    self.__line
                )
            )
        )
        self.__sentences.pop()

    def __integrate(self):
        firstSent = self.__sentences.pop(0)
        if self.__lastLineComplete:
            if len(firstSent) < 10:
                if len(self.__sentences) != 0:
                    self.__sentences[0] = firstSent + self.__sentences[0]
                else:
                    self.__sentences.insert(0, firstSent)
            else:
                self.__sentences.insert(0, firstSent)
        else:
            self.__last_tail = firstSent

    def append(self, tail):
        if tail is not None:
            self.__sentences[-1] += ' ' + tail

    def get_sentences(self):
        return self.__sentences
    
    def is_complete(self):
        try:
            return self.__sentences[-1].strip()[-1] == '.'
        except IndexError:
            return True
    
    def get_last_tail(self):
        return self.__last_tail

def segmentation(inputPath, outputPath):
    with open(inputPath, encoding='utf-8') as f:
        lines = f.readlines()

    handlers = []
    pre_line = LineHandler(lines[0], True)
    for i in range(1, int(len(lines)/2)):
        cur_line = LineHandler(lines[2*i], pre_line.is_complete())
        pre_line.append(cur_line.get_last_tail())
        handlers.append(pre_line)
        pre_line = cur_line
    handlers.append(pre_line)

    with open(outputPath, 'w', encoding='utf-8') as f:
        for handler in handlers:
            for sent in handler.get_sentences():
                f.write(sent + '\n')


if __name__ == '__main__':
    with open('./output/outputFile.txt', encoding='utf-8') as f:
        lines = f.readlines()

    handlers = []
    pre_line = LineHandler(lines[0], True)
    for i in range(1, int(len(lines)/2)):
        cur_line = LineHandler(lines[2*i], pre_line.is_complete())
        pre_line.append(cur_line.get_last_tail())
        handlers.append(pre_line)
        pre_line = cur_line
    handlers.append(pre_line)

    with open('result.txt', 'w', encoding='utf-8') as f:
        for handler in handlers:
            for sent in handler.get_sentences():
                f.write(sent + '\n')


    