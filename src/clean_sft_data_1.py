import json
import re

def clean_input(text):
    # `</think>` の後の文章のみを取得
    cleaned_text = re.split(r'</think>', text, maxsplit=1)[-1].strip()
    # 改行や空白を削除し、文章の開始部分を取得
    cleaned_text = re.sub(r'^\s+', '', cleaned_text)
    return cleaned_text

def process_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        if 'input' in item:
            item['input'] = clean_input(item['input'])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    input_json_path = "./data/text_1.json"
    output_json_path = "./data/text_2.json"
    process_json_file(input_json_path, output_json_path)
