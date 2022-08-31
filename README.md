# Bad Apple (NES)

Complete disassembly information (mostly) for the [Bad Apple](https://www.romhacking.net/homebrew/112/) NES homebrew created by [Litle Limit](https://web.archive.org/web/20190201082323/http://www.geocities.jp/littlimi/). Through clever programming, it plays the full movie at a crisp 30fps, accompanied by a chiptune recreation of the classic song, contributed by KARA.

This project was inspired by the [Nesdev wiki](https://www.nesdev.org/wiki/Bad_Apple) page on an earlier version of the ROM, which described the video format it used. Since this version (2.5) had purportedly not been cracked, I wanted to see for myself what tricks it used.

This was created through heavy use of the [Mesen](mesen.ca) debugger. Writeups for the more interesting internals can be found (eventually) in the `docs` directory.

This repository can also be used to generate a full disassembly of the rom itself, once included. In addition, utilities that generate the video and audio files are included, which more clearly demonstrate the compression algorithms used (in addition to verifying the correctness of the assembly).

## Setup

Since the rom is not provided in the repository, you'll have to place it here yourself by extracting the `.nes` file here from [here](https://www.romhacking.net/download/homebrew/112/). The correct rom has a SHA1 hash of `18d5801dd91db9fb769bbe8d3f714b83c7f0aa49`. Then, run `python3 disasm.py [your rom].nes` to create the assembly.
