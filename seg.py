import os
import re
import argparse
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, List, Optional

from julius4seg import converter, sp_inserter
from julius4seg.sp_inserter import ModelType, frame_to_second, space_symbols
import pyopenjtalk

def run_segment(
    wav_file: Path,
    input_yomi_file: Path,
    output_seg_file: Path,
    hmm_model: str,
    options: Optional[List[str]],
):
    utt_id = wav_file.name.split(".")[0]

    tmp_wav_file = NamedTemporaryFile(suffix=wav_file.suffix, delete=False)
    subprocess.run(
        f"sox {wav_file} -r 16k -c 1 -e signed "
        f"-b 16 {tmp_wav_file.name}",
        shell=True,
    )
    wav_file = Path(tmp_wav_file.name)

    with input_yomi_file.open() as f:
        base_yomi_text = f.readline().strip()

    julius_phones = re.split('\s*pau\s*', pyopenjtalk.g2p(base_yomi_text).lower())
    base_kan_text = ["sym_{}".format(i) for i in range(len(julius_phones))]

    assert len(base_kan_text) == len(
        julius_phones
    ), f"{base_kan_text}\n{julius_phones}"

    dict_1st = sp_inserter.gen_julius_dict_1st(
        base_kan_text, julius_phones, ModelType.gmm
    )
    dfa_1st = sp_inserter.gen_julius_dfa(dict_1st.count("\n"))

    with open(f"/tmp/first_pass_{utt_id}.dict", "w") as f:
        f.write(dict_1st)

    with open(f"/tmp/first_pass_{utt_id}.dfa", "w") as f:
        f.write(dfa_1st)

    raw_first_output = sp_inserter.julius_sp_insert(
        str(wav_file), f"/tmp/first_pass_{utt_id}", hmm_model, ModelType.gmm, options
    )

    forced_text_list = []
    forced_phones_list = []

    try:
        _, sp_position = sp_inserter.get_sp_inserted_text(raw_first_output)

        for j, (t, p) in enumerate(zip(base_kan_text, julius_phones)):
            forced_text_list.append(t)
            forced_phones_list.append(p)
            if j in sp_position:
                forced_text_list.append("<sp>")
                forced_phones_list.append(space_symbols[ModelType.gmm])

        forced_text_with_sp = " ".join(forced_text_list)
        forced_phones_with_sp = " ".join(forced_phones_list)
    except Exception:
        pass

    phones_with_sp = sp_inserter.get_sp_inserterd_phone_seqence(
        raw_first_output, ModelType.gmm
    )

    if len(forced_phones_with_sp) < 2:
        forced_phones_with_sp = phones_with_sp

    dict_2nd = sp_inserter.gen_julius_dict_2nd(forced_phones_with_sp, ModelType.gmm)
    dfa_2nd = sp_inserter.gen_julius_aliment_dfa(dict_2nd.count("\n"))

    with open(f"/tmp/second_pass_{utt_id}.dict", "w") as f:
        f.write(dict_2nd)

    with open(f"/tmp/second_pass_{utt_id}.dfa", "w") as f:
        f.write(dfa_2nd)

    raw_second_output = sp_inserter.julius_phone_alignment(
        str(wav_file), f"/tmp/second_pass_{utt_id}", hmm_model, ModelType.gmm, options
    )

    time_alimented_list = sp_inserter.get_time_alimented_list(raw_second_output)
    time_alimented_list = frame_to_second(time_alimented_list)
    assert len(time_alimented_list) > 0, raw_second_output

    with output_seg_file.open("w") as f:
        for ss in time_alimented_list:
            f.write("\t".join(list(ss)) + "\n")

    if tmp_wav_file is not None:
        tmp_wav_file.close()


def main():
    parser = argparse.ArgumentParser("sp insert demo by Julius")

    parser.add_argument("wav_file", type=Path, help="入力音声")
    parser.add_argument("input_yomi_file", type=Path, help="スペース区切りの読みファイル")
    parser.add_argument("output_seg_file", type=Path, help="時間情報付き音素セグメントファイル")

    parser.add_argument("--hmm_model", default=os.environ["HMM_MODEL"])
    parser.add_argument("--options", nargs="*", help="additional julius options")

    args = parser.parse_args()

    run_segment(**vars(args))

if __name__ == "__main__":
    main()
