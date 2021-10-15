Show Twitch chat messages as subtitles when watching Twitch Live with mpv.

Based on [mpv Twitch Chat](https://github.com/CrendKing/mpv-twitch-chat/) for VODs, but since `mpv-twitch-chat` uses Twitch API to retrieve comments history, it doesn't support live chat comments. This script uses a python subprocess to keep a background irc connection to a channel and dump last 10 messages to file in SubRip format.

## Issues

* Subtitle track is deleted and re-added on every refresh, so it blinks.

## Requirement

python3

## Install

`git clone` or download and unpack to mpv's `scripts` directory.

## TODO

Remove python dependancy: re-write in Lua using [lua-irc-engine](https://github.com/mirrexagon/lua-irc-engine) and [luasocket](https://github.com/diegonehab/luasocket).

## Usage

To activate the script, play a Twitch Live and switch on the "Twitch Chat" subtitle track. The script will replace it with its own subtitle track.

You can use mpv's auto profiles to conditionally apply special subtitle options when Twitch Live is on. For example,
```
[twitch]
profile-cond=get("path", ""):find("^https://w?w?w?%.?twitch%.tv/") ~= nil
profile-restore=copy-equal
sub-font-size=25
sub-align-x=right
sub-align-y=top
```
makes the Twitch chat subtitles smaller than default, and moved to the top right corner.