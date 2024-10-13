from pathlib import Path
import re

PARENT_DIR = Path(__file__).resolve().parent
INPUT_DIR = PARENT_DIR / "inputs"
OUTPUT_DIR = PARENT_DIR / "outputs"
LOG_DIR = PARENT_DIR / "logs"

input_file_name = "input.txt"
input_file_path = INPUT_DIR / input_file_name

FURIGANA_REGEX = re.compile(r'\{(.*?)\|(.*?)\}')

class Vocab:
    def __init__(self, md_vocab, meaning):
        self.width = 0
        self.md_vocab = md_vocab
        self.meaning = meaning
        self.components = self.split(md_vocab)
        self.no_furigana, self.anki_furigana, self.pronunciation = self.convert_formats()
    
    def __str__(self):
        return f"{self.no_furigana}({self.pronunciation}) - {self.meaning}"
    
    def csv_format(self):
        return f"{self.no_furigana},{self.md_vocab},{self.anki_furigana},{self.pronunciation},{self.meaning}"

    def split(self, vocab):
        split_result = re.split(r'(\{.*?\|.*?\})', vocab)
        split_result = [part.strip() for part in split_result if part.strip()]
        return split_result

    def calculate_segment_width(self, segment, furigana=""):
        base_len = len(segment) * 2
        if (furigana):
            extra_furigana = max(len(furigana) - base_len, 0)
            return base_len + extra_furigana
        parens = re.search(r'(\(|\))', segment)
        if parens:
            base_len -= 2 # parens are only half width
        return base_len

    def convert_formats(self):
        no_furigana= ""
        anki_furigana = ""
        pronunciation = ""
        i = 0
        for i in range(len(self.components)):
            part = self.components[i]
            if FURIGANA_REGEX.match(part):
                furigana = FURIGANA_REGEX.match(part)
                no_furigana += f"{furigana.group(1)}"
                pronunciation += f"{furigana.group(2)}"
                self.width += self.calculate_segment_width(furigana.group(1), furigana.group(2))
                if (i != 0):
                    anki_furigana += "[ ]"
                anki_furigana += f"{furigana.group(1)}[{furigana.group(2)}]"
            else:
                self.width += self.calculate_segment_width(part)
                no_furigana += part
                anki_furigana += part
                pronunciation += part
        return no_furigana, anki_furigana, pronunciation

def extract_vocab(text):
    text = text.strip().replace("- [  ] ", "").replace("*", "")
    text = text.replace("（", "(").replace("）", ")")
    vocab, meaning = re.split(r'[ 　]\-+[ 　]', text)
    return Vocab(vocab, meaning)

def format_vocab_list(vocab_list):
    formatted_list = []
    # format list so meaning lines up with vocab padding space with -
    for vocab in vocab_list:
        padding = "-" * (20 - vocab.width)
        formatted_list.append(f"{vocab.md_vocab} *{padding}* {vocab.meaning}")
    return formatted_list

def export_csv(vocab_list):
    with open(OUTPUT_DIR / "output.csv", "w") as file:
        for vocab in vocab_list:
            file.write(f"{vocab.csv_format()}\n")

def export_md(vocab_list):
    formatted_list = format_vocab_list(vocab_list)
    with open(OUTPUT_DIR / "output.md", "w") as file:
        for vocab in formatted_list:
            file.write(f"{vocab}\n")

def export_anki(vocab_list):
    with open(OUTPUT_DIR / "anki.txt", "w") as file:
        for vocab in vocab_list:
            file.write(f'{vocab.anki_furigana},{vocab.meaning},"","",""\n')

def build_vocab_list():
    with open(input_file_path, "r") as file:
        lines = file.readlines()
    vocab_list = []
    for line in lines:
        vocab = extract_vocab(line)
        vocab_list.append(vocab)
    export_csv(vocab_list)
    export_md(vocab_list)
    export_anki(vocab_list)


def main():
    build_vocab_list()

if __name__ == "__main__":
    main()