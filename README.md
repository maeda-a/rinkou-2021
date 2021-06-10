# rinkou-2021

## jp/ac/tsukuba/cs/ialab/postfix フォルダ

2020年度の輪講で用いた"Design Concepts in Programming Languages"に出てくるプログラミング言語の「構文木」と「操作的意味論」の実装の例．

現在は，PostFixの抽象構文木と，SmallStep操作的意味論の単純な実装例が入っている．
SmallStepのmainを実行すると，いくつかテストケースが実行される．

## pythonフォルダ

2021年度の輪講で用いている”Introduction to the Theory of Programming Languages"に出てくるプログラミング言語PCFの実装。
Jupyter notebookで対話的に試し、もう少し整理したバージョンをPCFフォルダにおいてある。

2021-06-10現在は、PCFフォルダ内にインタプリタ(3.2節および3.4.2節のバージョン)、コンパイラ(4.4節)、型検査器(5.1.2節)がある。

- Python 3.10 の構造パターンマッチングを使っている。3.10.0a6でテスト中。
- VS CodeのPython拡張 Pylance を満足させるには、settings.jsonに以下を記述する必要がある。

```Json
    "python.analysis.extraPaths": [
        "自分のワークスペースのフルパス/2021/python/PCF"
    ],
    "python.autoComplete.extraPaths": [
        "自分のワークスペースのフルパス/2021/python/PCF"
    ]
```