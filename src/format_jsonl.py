import json

def convert_to_jsonl(input_json_file, output_jsonl_file, id):
    with open(input_json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    with open(output_jsonl_file, "w", encoding="utf-8") as f:
        for item in data:
            jsonl_obj = {
                "ID": id,
                "messages": [
                    {"role": "system", "content": "以下は、タスクを説明する指示です。要求を適切に満たす応答を書きなさい。"},
                    {"role": "user", "content": item["input"]},
                    {"role": "assistant", "content": item["output"]}
                ]
            }
            f.write(json.dumps(jsonl_obj, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    id="text_1-1000_sft_1_1"
    input_json_path = "./data/text_1-1000_split_1_1/text_4.json"
    output_json_path = f"./data/text_1-1000_split_1_1/{id}.jsonl"
    
    convert_to_jsonl(input_json_path, output_json_path, id)
