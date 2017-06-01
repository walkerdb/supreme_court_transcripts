from pprint import pprint
from time import sleep
import os
import json

import requests
from tqdm import tqdm


def get_summaries():
    summary_json = requests.get("https://api.oyez.org/cases?per_page=0").json()
    write_json_to_file(summary_json, "oyez/all.json")


def get_cases():
    with open("oyez/all.json", mode="r") as f:
        data = json.load(f)

        for case_summary in tqdm(data):
            key = case_summary["ID"]
            case_data = requests.get(case_summary["href"])
            write_json_to_file(case_data, "oyez/cases/{}.json".format(key))
            sleep(0.5)


def get_transcripts():
    files = [f for f in os.listdir("oyez/cases") if f.endswith(".json")]
    files_to_iterate = {f for f in files if "t" not in f}
    ids_with_transcriptions = {f.split("-")[0] for f in files if "t" in f}
    ids_to_iterate = {f.split(".")[0] for f in files_to_iterate}.difference(ids_with_transcriptions)

    for id in tqdm(ids_to_iterate):
        data = get_json_from_file("oyez/cases/{}.json".format(id))
        audio_data = data.get("oral_argument_audio") or []
        for i, audio_file in enumerate(audio_data):
            transcript_data = requests.get(audio_file["href"]).json()
            filepath = "oyez/cases/{}-t{:02d}.json".format(id, i + 1)
            write_json_to_file(transcript_data, filepath)
            sleep(0.5)


def write_json_to_file(json_data, filepath):
    with open(filepath, mode="w") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)


def get_json_from_file(filepath):
    with open(filepath) as f:
        return json.load(f)


def rename_cases():
    all_files = {f for f in os.listdir("oyez/cases") if f.endswith(".json")}
    case_files = {f for f in all_files if "-" not in f}
    transcript_files = all_files.difference(case_files)
    for case in case_files:
        data = get_json_from_file("oyez/cases/{}".format(case))
        id = str(data.get("ID"))
        name = data.get("href").split("cases/")[-1].replace("-", "_").replace("/", ".")
        os.rename("oyez/cases/{}".format(case), "oyez/cases/{}.json".format(name))

        transcripts = [f for f in transcript_files if f.startswith(id)]
        for transcript in transcripts:
            number = transcript.split("-")[-1].replace(".json", "")
            os.rename("oyez/cases/{}".format(transcript), "oyez/cases/{}-{}.json".format(name, number))



if __name__ == "__main__":
    get_summaries()
    get_cases()
    get_transcripts()
