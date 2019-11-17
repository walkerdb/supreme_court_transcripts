# US Supreme Court Annotated Transcripts (auto-updated)

A dataset containing structured data on court cases presided by the justices of the United States Supreme Court, with transcripts for (nearly) every oral argument they've heard, annotated with audio timestamps and speaker identifications.
Includes links to digitized original audio from oral proceedings.

Data for each case is in a file named in the following pattern: `{year}.{docket #}.json`.
Transcripts for each hearing associated with that case have the same pattern, but appending `t01`, `t02`, etc.,
for each individual hearing.

Note that `docket #` normally is two numbers joined by `-`. In some cases, the actual docket number has a space
like `10 ORIG` and for those situations, the filename has a `_` in place of the space. Additionally, its
also worth noting that cases before 1955 do not seem to follow this pattern. Since the data before 1955 is 
incomplete anyways, it might be better to only focus on cases after.

For example, the overview for Roe v. Wade is given in `1971.70-18.json`. It had two separate oral arguments --
these two transcripts live in `1971.70-18-t01.json` and `1971.70-18-t02.json`.

At the end of each transcript json file is a `media_file` field, which contains an array of objects holding
Amazon s3 links to the digitized audio for that hearing in `mp3`, `ogg`, and `m3u8` formats.

## How to download?

You can `git clone` this repo but that is likely to be pretty slow. If you are only interested the data, 
you can head on over to the [releases](https://github.com/walkerdb/supreme_court_transcripts/releases)
where you can find weekly snapshots of this repo. Downloading these releases will be much quicker.
The archives are still pretty large, around 400MB. They decompress to about 3GB.

## Where does this come from?

All data retrieved on May 30, 2017 from [oyez.org](https://www.oyez.org)'s public api. Read more about the Oyez project [here](https://www.oyez.org/about).

[Licensed as CC-BY-NC to Oyez, Inc.](https://www.oyez.org/license), a collaboration of Cornell’s Legal Information Institute, Chicago-Kent College of Law, and Justia.com.

## Oyez API

Oyez has a wonderful but undocumented public API. Here's the gist of it:

You can look through `update.py` to see how this repo is auto-updated
which will also help you keep your local copies updated if you want.

-----------------------

The owner of this repo has no affiliation with the Oyez project -- just admiration!
