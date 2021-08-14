"""メルスペクトラムデータ作成
"""
import json
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd

from dataset.smdataset.parse import parse_sm_txt


class NotesData:
    def __init__(self):
        self.note_data = {
            "live_id": None,
            "live_difficulty_type": None,
            "title": None,
            "note_id": None,
            "timing_msec": None,
            "rail": None,
            "note_type": None,
            "diff": None,
            "bgm_path": None,
            "is_normal_note": None,
            "notes_duration(/beats)": None,
        }


def calculate_abs_time(elapsed_bar_count, relative_beats_count, bpm_info):
    elapsed_beats = elapsed_bar_count * 4 + relative_beats_count
    accumulated_time = 0
    n_bpms = len(bpm_info)
    for index, bpm in enumerate(bpm_info):
        if float(bpm[0]) < elapsed_beats:
            if index + 1 < n_bpms: # Not the final bpm
                accumulated_time += (bpm_info[index + 1][0] - bpm[0]) * 4 * 60000 / bpm[1]
            else: # The final bpm
                pass







if __name__ == "__main__":
    save_dir = "../data/score_onsets"
    future_list = []
    with ProcessPoolExecutor() as executor:
        for root, subdir, files in os.walk("../data/json_raw"):
            for file in files:
                if file.endswith(".json"):
                    note_data = []
                    with open(os.path.join(root, file)) as json_file:
                        json_info = json.load(json_file)
                    music_file_path = json_info['music_fp']
                    bpms = json_info['bpms']
                    sm_file_path = Path(json_info["sm_fp"])
                    live_id = json_info['pack'] + '_' + json_info['title']
                    with open(sm_file_path, 'r') as sm_file:
                        sm_content = parse_sm_txt(sm_file.read())
                        print(sm_content.keys())
                        for score in sm_content['notes']:
                            if score[0] == 'dance-single':
                                note_id = 1
                                score_type = score[0]
                                difficulty = score[2]
                                scores_data = score[5]
                                bar_count = 0
                                elapsed_time = 0
                                current_bpm = bpms[0][1]
                                for score_data in scores_data:  # Every bar is in this loop, and each bar has fixed 4 beats
                                    note_duration = len(score_data) // 4
                                    sub_beats_count = 0
                                    for sub_score in score_data:  # Every line/beats is in this loop
                                        total_elapsed_beats = bar_count + sub_beats_count
                                        for track_id, track_data in enumerate(sub_score):  # Go to track analysis here
                                            if track_data != '0':
                                                note_data.append({
                                                    "live_id": live_id,
                                                    "live_difficulty_type": difficulty,
                                                    "title": json_info['title'],
                                                    "note_id": note_id,
                                                    "timing_bar_main": bar_count,
                                                    "timing_bar_beats": sub_beats_count,
                                                    "rail": track_id + 1,
                                                    "note_type": track_data,
                                                    "timing_msec": None,
                                                    "bgm_path": music_file_path,
                                                    "is_normal_note": 1 if track_data == '1' else 0,
                                                    "notes_duration(/beats)": note_duration,
                                                })
                                                note_type = track_data
                                                note_id += 1
                                        sub_beats_count += 1 / note_duration
                                    bar_count += 1
                                print(score)
                    print("BPM: ", end='')
                    print(bpms)
                    bpm_df = pd.DataFrame(bpms, columns=['time', 'bpm'])
                    file_path = Path(os.path.join(save_dir, root.split('/')[-2], root.split('/')[-1], Path(file).stem))
