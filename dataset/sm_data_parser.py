import os

from smdataset.parse import parse_sm_txt

if __name__ == "__main__":
    with open('../data/raw/itg/In The Groove/PA Theme/PA Theme.sm','r') as sm_file:
        res_dict = parse_sm_txt(sm_file.read())
        for unit in (res_dict['notes']):
            if unit[0]=="dance-single":
                print(unit[2])
    # save_dir = "../data/mel_log"
    # for root, subdir, files in os.walk("../data/raw"):
    #     for file in files:
    #         if file.endswith(".sm"):
    #             with open(os.path.join(root, file), 'r') as sm_file:
    #                 print(os.path.join(root, file))
    #                 res_dict = parse_sm_txt(sm_file.read())
    #                 print(res_dict.keys())
    #                 break
    #         break
