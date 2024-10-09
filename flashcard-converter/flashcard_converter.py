# open file input.txt for read

input_file_name = "inputs/input.txt"

with open(input_file_name, "r") as file:
    lines = file.readlines()

# example of line: '- [ ] どうなりますか *-------* what will happen'
for line in lines:
    # remove newlines and '- [ ]' from the beginning of the line
    line = line.strip().replace("- [ ] ", "")
    import re
    vocab, meaning = re.split(r' \*\-+\* ', line)
    print(f"{vocab} - {meaning}")
    furigana_regex = re.compile(r'\{(.*?)\|(.*?)\}')
    split_result = re.split(r'(\{.*?\|.*?\})', vocab)
    split_result = [part.strip() for part in split_result if part.strip()]
    no_furigana= ""
    anki_furigana = ""
    i = 0
    for i in range(len(split_result)):
        part = split_result[i]
        if furigana_regex.match(part):
            furigana = furigana_regex.match(part)
            no_furigana += f"{furigana.group(1)}"
            if (i != 0):
                anki_furigana += "[ ]"
            anki_furigana += f"{furigana.group(1)}[{furigana.group(2)}]"
        else:
            no_furigana += part
            anki_furigana += part

    print(f"{no_furigana} - {anki_furigana}")

