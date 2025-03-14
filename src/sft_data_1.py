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
    
    # 各プロンプトに対して処理を行う
    for item in input_data:
        prompt = item["text"]
        prompt_text = f"""
あなたは質問生成の専門家です。
以下の文章は、ある質問に対する「回答」です。
この回答に対する適切な質問文を考えて日本語で出力してください。

回答文：
{prompt}

指示：
1. 回答の内容に合致する自然な質問文を作成してください
2. 質問は以下のいずれかの形式で終えること：  
    - 「何」「どのように」「なぜ」「どうして」「どんな」「どれくらい」などの疑問詞  
    - 「〜とは？」「〜について教えて」「〜の理由は？」「〜の仕組みは？」などの疑問形  
    - 「〜するにはどうすればいい？」や「〜の違いは？」などの比較・手順を問う形式  
3. 質問は1つだけ作成し、余計な説明は不要です
4. 質問文の後に余計なコメントや追加説明は加えないでください
"""
        
        # テキスト生成
        print(f"ID: {item['id']} のプロンプトを処理中...")
        response = generate_text(llm, prompt_text, max_tokens=4096, temperature=0.8)
        print(prompt_text)
        print(response)

        # 生成されたレスポンスから入力部分を抽出
        if response:
            input_text = extract_input_from_output(response)
            if input_text:
                # 結果をリストに追加
                results.append({
                    "input": input_text,
                    "output": prompt
                })
                print(f"ID: {item['id']} の処理が完了しました")
            else:
                print(f"ID: {item['id']} のinputの抽出に失敗しました")
        else:
            print(f"ID: {item['id']} の応答の生成に失敗しました")
    
    # 結果をJSONファイルに保存
    try:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"結果を {output_json_path} に保存しました")
    except Exception as e:
        print(f"出力JSONファイルの保存に失敗しました: {e}")

if __name__ == "__main__":
    model_path = "./model/Tifa-Deepsex-14b-CoT-Q4_K_M.gguf"
    input_json_path = "./input/text_1-1000_split_1_1.json"
    output_json_path = "./data/text_1-1000_split_1_1/text_1.json"
    #input_json_path = "./input/text_1-1000_split_1_1.json"
    #output_json_path = "./data/text_1-1000_sft_1.json"
    
    main(model_path, input_json_path, output_json_path)