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
                kanji_len = len(furigana.group(1)) * 2
                self.width += kanji_len
                extra_furigana = max(len(furigana.group(2)) - kanji_len, 0)
                self.width += extra_furigana
                if (i != 0):
                    anki_furigana += "[ ]"
                anki_furigana += f"{furigana.group(1)}[{furigana.group(2)}]"
            else:
                self.width += 2 * len(part)
                no_furigana += part
                anki_furigana += part
                pronunciation += part
        return no_furigana, anki_furigana, pronunciation

def extract_vocab(text):
    text = text.strip().replace("- [ ] ", "").replace("*", "")

    vocab, meaning = re.split(r' \-+ ', text)
    return Vocab(vocab, meaning)

def format_vocab_list(vocab_list):
    longest_vocab = max([vocab.width for vocab in vocab_list])
    min_length = 4
    formatted_list = []
    # format list so meaning lines up with vocab padding space with -
    for vocab in vocab_list:
        padding = "-" * (longest_vocab - vocab.width + min_length)
        formatted_list.append(f"{vocab.md_vocab} *{padding}* {vocab.meaning}")
    return formatted_list


def build_vocab_list():
    with open(input_file_path, "r") as file:
        lines = file.readlines()
    vocab_list = []
    for line in lines:
        vocab = extract_vocab(line)
        vocab_list.append(vocab)
    with open(OUTPUT_DIR / "output.csv", "w") as file:
        for vocab in vocab_list:
            file.write(f"{vocab.csv_format()}\n")
    formatted_list = format_vocab_list(vocab_list)
    with open(OUTPUT_DIR / "output.md", "w") as file:
        for line in formatted_list:
            file.write(f"{line}\n")

def main():
    build_vocab_list()

if __name__ == "__main__":
    main()