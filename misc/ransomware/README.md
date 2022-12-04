## ransomware
### 問題文
友人が誕生日祝いで送ってきたスクリプトを実行したら、お手製ランサムで手元のFlagを暗号化されてしまった...
実行されたスクリプトを共有するから、どうにかしてFlagを復元してほしい🙇‍♂️

※ローカルで無闇に実行しないでください！ローカルで実行すると関係のないファイルまで暗号化される可能性があります。

### 方針
- `taskctf{` のprefixは既知なので、その部分からXORに利用されたkeyを入手できる

## 難易度
beginner

## コメント
- xorがguess要素にならないように注意したい
- なんらかの数値を取得する部分はなくても解けるので、APIは実装しない
  - 実際のC2は検体をリバースエンジニアリングできた時点で落とされていることが多い