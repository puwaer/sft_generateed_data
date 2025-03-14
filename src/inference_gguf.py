from llama_cpp import Llama
import sys

def load_model(model_path):
    """
    GGUFモデルを読み込む関数
    """
    try:
        # Llamaクラスのインスタンスを作成
        # n_ctx: コンテキスト長
        # n_gpu_layers: GPU使用時のレイヤー数（環境に応じて調整）
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_gpu_layers=-1,  # CPUのみ使用する場合は0、GPU使用時は適宜調整
            verbose=True
        )
        return llm
    except Exception as e:
        print(f"モデルの読み込みに失敗しました: {e}")
        sys.exit(1)

def generate_text(llm, prompt, max_tokens=1024, temperature=0.7):
    """
    モデルを使用してテキストを生成する関数
    """
    try:
        # 推論の実行
        output = llm(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95,
            echo=False
        )
        return output['choices'][0]['text'].strip()
    except Exception as e:
        print(f"テキスト生成に失敗しました: {e}")
        return None

def main():
    # モデルファイルのパス（環境に合わせて変更してください）
    model_path = "./model/Tifa-Deepsex-14b-CoT-Q4_K_M.gguf"
    
    prompt = """
    以下の文章を回答文として出力するような疑問文を日本語で教えてください\n\n
    黄雷のガクトゥーン：シャイニングナイト-N'gha-Kthun：ShiningNight-
    """
        
    llm = load_model(model_path)
    
    # テキスト生成
    response = generate_text(llm, prompt, max_tokens=1024, temperature=0.7)
    
    # 結果の表示
    if response:
        print(response)
    else:
        print("応答の生成に失敗しました")

if __name__ == "__main__":
    main()

