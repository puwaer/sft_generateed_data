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
        if 'output' in item:
            item['output'] = clean_input(item['output'])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    input_json_path = "./data/text_3.json"
    output_json_path = "./data/text_4.json"
    process_json_file(input_json_path, output_json_path)
