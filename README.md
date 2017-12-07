hbbtv-dvbstream
===============

This project contains some scripts to generate a transport stream using FFMpeg and Opencaster which triggers HbbTV portals on a TV. 
The stream can be played using [vlc player](https://www.videolan.org/).

It is composed of tree files:

* *init-cmd.bat*: Makes preparations for cmd.exe.

* *make-stream.bat*: Generate the final transport stream. (First, it splits the mpeg files into different transport streams elements for audio and video. Second, it multiplexes the metadata tables, videos and audios streams into a final transport stream file)

* *create-metadata-ts.py*: Creates stream tables ( PAT, NIT, AIT, SDT, PMT) inspired by the opencaster hbbtv sample.



## Requirements

* [ffmpeg](http://ffmpeg.org)
* [opencaster](http://www.avalpa.com/the-key-values/15-free-software/33-opencaster)
* [python](https://www.python.org)

## Related Projects

[EBU Cross-Platform Authentication project](http://tech.ebu.ch/cpa)
[ebu-hbbtv-dvbstream](https://github.com/ebu/hbbtv-dvbstream)


## Contributors

* [Michael Barroco](https://github.com/barroco) (EBU)
* [Gökhan Erdoğdu](https://github.com/GERD0GDU)


## Copyright & License

Copyright (c) 2014, EBU-UER Technology & Innovation

The code is under BSD (3-Clause) License. (see LICENSE.txt)
