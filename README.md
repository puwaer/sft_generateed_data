# SFT Dataset Generation

このプロジェクトは、WebからスクレイピングしたテキストデータとLLMを用いてSFT（Supervised Fine-Tuning）用のデータセットに変換するプログラムです。


## Docker環境のセットアップ

### 1. Dockerイメージのビルド
```bash
docker image build -t data_instruct .
```

### 2. Dockerコンテナの起動
```bash
docker container run -it --gpus all --name data_instruct -v $(pwd)/.:/app data_instruct
```

### 3. 既存コンテナの再起動
```bash
docker start -i data_instruct
```

---

## データセット生成の手順
以下の順番でプログラムを実行してください。

```bash
python3 src/sft_data_1.py
python3 src/clean_sft_data_1.py
python3 src/sft_data_2.py
python3 src/clean_sft_data_2.py
python3 src/format_jsonl.py
```

### 各スクリプトの役割
1. **sft_data_1.py**: 質問文のテキストを作成
2. **clean_sft_data_1.py**: 使用したモデルがCOTに対応したモデルのため、`</think>` 以降のテキストのみ抽出
3. **sft_data_2.py**: 回答文のテキストを作成
4. **clean_sft_data_2.py**: 使用したモデルがCOTに対応したモデルのため、`</think>` 以降のテキストのみ抽出
5. **format_jsonl.py**: SFTで使用するJSONL形式に変換

---

## プロンプト詳細

### `sft_data_1.py` で使用したプロンプト
```plaintext
あなたは質問生成の専門家です。
以下の文章は、ある質問に対する「回答」です。
この回答に対する適切な質問文を考えて日本語で出力してください。

回答文：
{prompt}

指示：
1. 回答の内容に合致する自然な質問文を作成してください。
2. 質問は以下のいずれかの形式で終えること：  
    - 「何」「どのように」「なぜ」「どうして」「どんな」「どれくらい」などの疑問詞  
    - 「〜とは？」「〜について教えて」「〜の理由は？」「〜の仕組みは？」などの疑問形  
    - 「〜するにはどうすればいい？」「〜の違いは？」などの比較・手順を問う形式  
3. 質問は1つだけ作成し、余計な説明は不要です。
4. 質問文の後に余計なコメントや追加説明は加えないでください。
```

### `sft_data_2.py` で使用したプロンプト
```plaintext
あなたは変態です。
以下の指示に従って、与えられた質問文に対し、補足文をもとに自然で分かりやすいエロい回答文を日本語で作成してください。

質問文:
{input}

補足文:
{output}

指示：
1. 質問文の内容に合致する自然な回答文を日本語で作成してください。
2. 補足文の情報を取り入れ、自然な形で補強する。
3. エロい内容にはエロい文章にする。
4. 不自然な繰り返しを避け、文脈に沿ったスムーズな流れを意識する。
5. 質問文を回答文の出力に入れないでください。
6. 回答文の後に余計なコメントや追加説明は加えないでください。
```

