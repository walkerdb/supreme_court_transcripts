# US Supreme Court Annotated Transcripts (auto-updated)

A dataset containing structured data on court cases presided by the justices of the United States Supreme Court, with transcripts for (nearly) every oral argument they've heard, annotated with audio timestamps and speaker identifications.
Includes links to digitized original audio from oral proceedings.

The data self-updates every Saturday using a [github action](https://github.com/walkerdb/supreme_court_transcripts/blob/master/.github/workflows/auto-update.yml). 
If you just want the raw data check out the [releases tab](https://github.com/walkerdb/supreme_court_transcripts/releases), 
which updates on the same schedule. You'll need ~3.5GB of free disk space to decompress the full archive. 

Many thanks to [@azeemba](https://github.com/azeemba) for getting the auto-update system in place.

## Data structure

Data for each case is in a file named in the following pattern: `{year}.{docket #}.json`.
Transcripts for each hearing associated with that case have the same pattern, but appending `t01`, `t02`, etc.,
for each individual hearing.

For example, the overview for Roe v. Wade is given in `1971.70-18.json`. It had two separate oral arguments --
these two transcripts live in `1971.70-18-t01.json` and `1971.70-18-t02.json`.

At the end of each transcript json file is a `media_file` field, which contains an array of objects holding
Amazon s3 links to the digitized audio for that hearing in `mp3`, `ogg`, and `m3u8` formats.

Note that `docket #` normally is two numbers joined by `-`. In some cases, the actual docket number has a space
like `10 ORIG`. In those situations the filename has a `_` in place of the space. Cases before 1955 do not seem 
to follow this pattern, and in general are less complete than cases after.

## Where does this come from?

All data retrieved on May 30, 2017 from [oyez.org](https://www.oyez.org)'s public api. Read more about the Oyez project [here](https://www.oyez.org/about).

[Licensed as CC-BY-NC to Oyez, Inc.](https://www.oyez.org/license), a collaboration of Cornell’s Legal Information Institute, Chicago-Kent College of Law, and Justia.com.

## Oyez API

Oyez has a wonderful but undocumented public API. Here's the gist of it:

To retrieve all case summaries (the equivalent of the `case_summaries.json` file):  
`https://api.oyez.org/cases?per_page=0`

If you don't want everything you can add a term filter, like the following:  
`https://api.oyez.org/cases?per_page=0&filter=term:1965`

That data will hold links to get further info on each case. eg:  
`https://api.oyez.org/cases/1965/14_orig`

The format here is generally `api.oyez.org/cases/{term}/{docket_number}`

The "oral_argument_audio" field in this case-specific response holds links to the audio and transcriptions for each hearing - this data is what is saved in the transcription files in the repo. eg:  
`https://api.oyez.org/case_media/oral_argument_audio/14026`

The [update.py](./update.py) script uses this API to auto-update this repo.
You can also use it to help you keep your local copies updated.

-----------------------

The owner of this repo has no affiliation with the Oyez project -- just admiration!
