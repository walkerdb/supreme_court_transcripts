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

## License
 
All data provided by Oyez, Inc., under CC-BY-NC. Check out their (awesome) site at [oyez.org](https://www.oyez.org)! 