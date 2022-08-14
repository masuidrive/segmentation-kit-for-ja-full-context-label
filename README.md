# 時間付きフルコンテキストラベル生成ツール

[julius4seg](https://github.com/Hiroshiba/julius4seg)と[pyopenjtalk](https://github.com/r9y9/pyopenjtalk)を呼び出して、下記のような時間付きフルコンテキストラベルを生成します。

```
0 2925000 xx^xx-sil+m=i/A:xx+xx+xx/B:xx-xx_xx/C:xx_xx+xx/D:02+xx_xx/E:xx_xx!xx_xx-xx/F:xx_xx#xx_xx@xx_xx|xx_xx/G:3_3%0_xx_xx/H:xx_xx/I:xx-xx@xx+xx&xx-xx|xx+xx/J:5_23/K:1+5-23
2925000 3525000 xx^sil-m+i=z/A:-2+1+3/B:xx-xx_xx/C:02_xx+xx/D:13+xx_xx/E:xx_xx!xx_xx-xx/F:3_3#0_xx@1_5|1_23/G:7_2%0_xx_1/H:xx_xx/I:5-23@1+1&1-5|1+23/J:xx_xx/K:1+5-23
3525000 4225000 sil^m-i+z=u/A:-2+1+3/B:xx-xx_xx/C:02_xx+xx/D:13+xx_xx/E:xx_xx!xx_xx-xx/F:3_3#0_xx@1_5|1_23/G:7_2%0_xx_1/H:xx_xx/I:5-23@1+1&1-5|1+23/J:xx_xx/K:1+5-23
4225000 5325000 m^i-z+u=o/A:-1+2+2/B:xx-xx_xx/C:02_xx+xx/D:13+xx_xx/E:xx_xx!xx_xx-xx/F:3_3#0_xx@1_5|1_23/G:7_2%0_xx_1/H:xx_xx/I:5-23@1+1&1-5|1+23/J:xx_xx/K:1+5-23
```

## 準備

基本的には Docker から呼び出すことを想定しています。

```
git clone https://github.com/masuidrive/segmentation-kit-for-ja-full-context-label.git
cd segmentation-kit-for-ja-full-context-label
docker build --tag s4fcl .
```

## 起動

使い方は二種類です

### 現在のディレクトリ上の.wav ファイルを全て変換する

```
docker --tty --rm `pwd`:/data s4fcl
```

現在のディレクトリの`.wav`ファイルと同名の`.txt`ファイルを読み込んで、`.lab`ファイルにフルコンテキストラベルを生成します。

例えば、`BASIC5000_0001.txt`が下記のようなファイルで、それを読み上げた音声ファイルが`BASIC5000_0001.wav`にある場合、`BASIC5000_0001.lab`というフルコンテキストラベルファイルが生成されます。

```
水をマレーシアから買わなくてはならないのです
```

### 現在のディレクトリ上の.wav ファイルを全て変換する

```
docker --tty --rm `pwd`:/data s4fcl /data/sample1.wav  /data/sample2.txt  /data/sample3.lab
```

上記のように音声、読み、出力ファイルのパスを指定して単一のファイルを処理することもできます。

---

Yuichiro Masui
https://github.com/masuidrive
