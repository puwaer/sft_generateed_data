from llama_cpp import Llama
import sys
import json
import re

def load_model(model_path, seed=42):
    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_gpu_layers=-1,
            verbose=True,
            seed=seed  # 乱数シードを固定
        )
        return llm
    except Exception as e:
        print(f"モデルの読み込みに失敗しました: {e}")
        sys.exit(1)

def generate_text(llm, prompt, max_tokens=4096, temperature=0.8):
    """
    モデルを使用してテキストを生成する関数
    """
    try:
        output = llm(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95,
            top_k=40,
            repeat_penalty=1.1,
            echo=False
        )
        return output['choices'][0]['text'].strip()
    except Exception as e:
        print(f"テキスト生成に失敗しました: {e}")
        return None

def extract_input_from_output(output_text):
    """
    出力から</think>以降の部分をinputとして抽出する関数
    """
    match = re.search(r"</think>\s*(.+)", output_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def main(model_path, input_json_path, output_json_path):
    # 入力JSONファイルを読み込む
    try:
        with open(input_json_path, "r", encoding="utf-8") as f:
            input_data = json.load(f)
    except Exception as e:
        print(f"入力JSONファイルの読み込みに失敗しました: {e}")
        sys.exit(1)
    
    # モデルの読み込み
    llm = load_model(model_path)
    
    # 結果を格納するリスト
    results = []
    id = 0
    
    # 各プロンプトに対して処理を行う
    for item in input_data:
        input = item["input"]
        output = item["output"]
        prompt_text = f"""
あなたは変態です。
以下の指示にしたがって、与えられた質問文に対し、補足文をもとに自然で分かりやすいエロい回答文を日本語で作成してください。

質問文:
{input}

補足文:
{output}

指示：
1. 質問文の内容に合致する自然な回答文を日本語で作成してください
2. 補足文の情報を取り入れ、自然な形で補強する
3. エロい内容にはエロい文章にする
4. 不自然な繰り返しを避け、文脈に沿ったスムーズな流れを意識する
5. 質問文を回答文の出力に入れないください
6. 回答文の後に余計なコメントや追加説明は加えないでください
"""
        
        # テキスト生成
        id = id + 1
        print(f"ID: {id} のプロンプトを処理中...")
        response = generate_text(llm, prompt_text, max_tokens=4096, temperature=0.8)
        print(prompt_text)
        print(response)

        # 生成されたレスポンスから入力部分を抽出
        if response:
            output_text = extract_input_from_output(response)
            if output_text:
                # 結果をリストに追加
                results.append({
                    "input": input,
                    "output": output_text
                })
                print(f"ID: {id} の処理が完了しました")
            else:
                print(f"ID: {id} のoutputの抽出に失敗しました")
        else:
            print(f"ID: {output} の応答の生成に失敗しました")
    
    # 結果をJSONファイルに保存
    try:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"結果を {output_json_path} に保存しました")
    except Exception as e:
        print(f"出力JSONファイルの保存に失敗しました: {e}")

if __name__ == "__main__":
    model_path = "./model/Tifa-Deepsex-14b-CoT-Q4_K_M.gguf"
    input_json_path = "./data/text_2.json"
    output_json_path = "./data/text_3.json"
    
    main(model_path, input_json_path, output_json_path)