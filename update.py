#!/usr/bin/env python3
"""
Script to find new/missing cases and update
the repo with that
"""

import json
from datetime import date
import traceback

import requests
from ratelimit import limits, sleep_and_retry

YEARS_TO_GO_BACK = 2


@sleep_and_retry
@limits(calls=10, period=10)  # no more than 1 call per second
def get_http_json(url):
    print(f"Getting {url}")
    response = requests.get(url)
    parsed = response.json()
    return parsed


def get_case(term, docket):
    """Get the info of the case and fetch all
    transcripts that the info links to"""
    url = f"https://api.oyez.org/cases/{term}/{docket}"
    docket_data = get_http_json(url)

    oral_argument_audio = docket_data["oral_argument_audio"]
    transcripts = []
    for link in oral_argument_audio:
        t = get_http_json(link["href"])
        transcripts.append(t)

    return docket_data, transcripts


def write_case(term, docket, docket_data, transcripts):
    """
    Writes term-docket.json file with docket_data
    For each transcript, writes the term-docket-t##.json file
    """
    with open(f"oyez/cases/{term}.{docket}.json", "w") as docket_file:
        json.dump(docket_data, docket_file, indent=2)

    count = 0
    for t in transcripts:
        count += 1
        t_filename = "oyez/cases/{}.{}-t{:0>2d}.json".format(term, docket, count)
        with open(t_filename, "w") as t_file:
            json.dump(t, t_file, indent=2)


def fetch_missing(cases):
    """
    cases is a map of tuples to Summary (term, docket) : {SUMMARY}
    For each case, fetch the docket and transcript data and write to a file
    
    return set of cases that this was succesful for
    """
    count = 0
    total = len(cases)
    succesful = set()
    for term, docket in cases.keys():
        ## pull the file
        count += 1
        print(f"Trying: {term}/{docket}\t\t{count}/{total}")
        try:
            docket_data, transcripts = get_case(term, docket)
            write_case(term, docket, docket_data, transcripts)
            succesful.add((term, docket))
        except Exception as exc:
            traceback.print_exc()
            print(f"Failed for {term}/{docket}, continuing anyways")
    return succesful


def load_known_cases():
    with open("oyez/case_summaries.json") as handle:
        known_summaries = json.load(handle)
    known_map = {
        (summary["term"], summary["docket_number"]): summary
        for summary in known_summaries
    }
    return (known_summaries, known_map)


def find_missing(known_map, years):
    """
    Fetch all summaries for given years and find any that are
    missing in the local "known_map"
    """
    to_fetch = {}
    for year in years:
        summary_url = f"https://api.oyez.org/cases?per_page=0&filter=term:{year}"
        summaries = get_http_json(summary_url)
        for summary in summaries:
            if (summary["term"], summary["docket_number"]) not in known_map:
                to_fetch[(summary["term"], summary["docket_number"])] = summary

    return to_fetch


def years_to_recheck():
    """
    Makes a list of years going back to
    YEARS_TO_GO_BACK
    e.g. [2018, 2019]
    """
    cur_year = date.today().year
    return list(range(cur_year - YEARS_TO_GO_BACK + 1, cur_year))


def main():
    """
    Find any cases that the server is updated with but we don't have locally
    and fetch the case info and transcripts for them.
    For all cases this is succesful for, also update case_summaries
    """
    (known_summaries, known_map) = load_known_cases()
    missing_summaries = find_missing(known_map, years_to_recheck())

    print(f"Missing {len(missing_summaries)} cases")
    print(missing_summaries.keys())

    succesful = fetch_missing(missing_summaries)

    for term, docket in succesful:
        known_summaries.append(missing_summaries[(term, docket)])

    print(f"Updated {len(succesful)} records!")
    if len(succesful) > 0:
        with open("oyez/case_summaries.json", "w") as handle:
            json.dump(known_summaries, handle, indent=2)


if __name__ == "__main__":
    main()
