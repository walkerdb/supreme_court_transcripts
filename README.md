# Supreme Court Annotated Transcripts

A dataset of supreme court transcripts annotated with audio timestamps and speaker identifications.
Includes links to digitized original audio from oral proceedings.

Data for each case is in a file named in the following pattern: `{year}.{docket #}.json`.
Transcripts for each hearing associated with that case have the same pattern, but appending `t01`, `t02`, etc.,
for each individual hearing.

For example, the overview for Roe v. Wade is given in `1971.70-18.json`. It had two separate oral arguments --
these two transcripts live in `1971.70-18-t01.json` and `1971.70-18-t02.json`.

At the end of each transcript json file is a `media_file` field, which contains an array of objects holding
Amazon s3 links to the digitized audio for that hearing in `mp3`, `ogg`, and `m3u8` formats.

## Oyez API
It's not documented on the site, but here is the gist of it:

To retrieve all case summaries (the equivalent of the `case_summaries.json` file):  
`https://api.oyez.org/cases?per_page=0`

If you don't want everything you can add a term filter, like the following:  
`https://api.oyez.org/cases?per_page=0&filter=term:1965`

That data will hold links to get further info on each case. eg:  
`https://api.oyez.org/cases/1965/14_orig`

The format here is generally `api.oyez.org/cases/{term}/{docket_number}`

The "oral_argument_audio" field in this case-specific response holds links to the audio and transcriptions for each hearing - this data is what is saved in the transcription files in the repo. eg:  
`https://api.oyez.org/case_media/oral_argument_audio/14026`

## Provenance & License

All data retrieved on May 30, 2017 from [oyez.org](https://www.oyez.org)'s public api. Read more about the Oyez project [here](https://www.oyez.org/about).

[Licensed as CC-BY-NC to Oyez, Inc.](https://www.oyez.org/license), a collaboration of Cornell’s Legal Information Institute, Chicago-Kent College of Law, and Justia.com.

The owner of this repo has no affiliation with the Oyez project -- just admiration!
