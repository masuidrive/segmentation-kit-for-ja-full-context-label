# Dockerfileから呼ばれて、pyopenjtalkの辞書をダウンロードする
import pyopenjtalk

# load dictionary
pyopenjtalk.g2p("あ")