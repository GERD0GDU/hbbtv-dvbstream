SET VIDEOFILE1="C:\Users\gerdogdu\Videos\hbbtv\video1.mp4"
SET VIDEOFILE2="C:\Users\gerdogdu\Videos\hbbtv\video2.mp4"

IF NOT EXIST ".\output" (
	MKDIR ".\output"
)

IF NOT EXIST ".\tmp" (
	MKDIR ".\tmp"
)

;VIDEOFILE1

ffmpeg -i %VIDEOFILE1% -ss 00:00:00 -t 00:00:50 -async 1 -r 25 -an -vcodec mpeg2video -f mpeg2video -b 5000k -maxrate 5000k -minrate 5000k -bf 2 -bufsize 1835008 -y ".\output\video1.mp2"

esvideompeg2pes ".\output\video1.mp2" > ".\output\video1.pes"
pesvideo2ts 2001 25 112 5247425 0 ".\output\video1.pes" > ".\output\video1.ts"

ffmpeg -i %VIDEOFILE1% -ss 00:00:00 -t 00:00:50 -async 1 -r 25 -ac 2 -vn -acodec mp2 -f mp2 -ab 128000 -ar 48000 -y ".\output\audio1.mp2"

esaudio2pes ".\output\audio1.mp2" 2304 48000 768 -1 3600 > ".\output\audio1.pes"
pesaudio2ts 2101 2304 48000 768 -1 ".\output\audio1.pes" > ".\output\audio1.ts"

;VIDEOFILE2

ffmpeg -i %VIDEOFILE2% -ss 00:00:00 -t 00:00:50 -async 1 -r 25 -an -vcodec mpeg2video -f mpeg2video -b 5000k -maxrate 5000k -minrate 5000k -bf 2 -bufsize 1835008 -y ".\output\video2.mp2"

esvideompeg2pes ".\output\video2.mp2" > ".\output\video2.pes"
pesvideo2ts 2002 25 112 5247425 0 ".\output\video2.pes" > ".\output\video2.ts"

ffmpeg -i %VIDEOFILE2% -ss 00:00:00 -t 00:00:50 -async 1 -r 25 -ac 2 -vn -acodec mp2 -f mp2 -ab 128000 -ar 48000 -y ".\output\audio2.mp2"

esaudio2pes ".\output\audio2.mp2" 2304 48000 768 -1 3600 > ".\output\audio2.pes"
pesaudio2ts 2102 2304 48000 768 -1 ".\output\audio2.pes" > ".\output\audio2.ts"

python ".\create-metadata-ts.py"

tscbrmuxer c:5247425 ".\output\video1.ts" b:156000 ".\output\audio1.ts" b:5247425 ".\output\video2.ts" b:156000 ".\output\audio2.ts" b:19024 ".\output\pat.ts" b:18724 ".\output\pmt0.ts" b:18724 ".\output\pmt1.ts" b:1400 ".\output\nit.ts" b:1500 ".\output\sdt.ts" b:18724 ".\output\ait0.ts" b:18724 ".\output\ait1.ts" > ".\output\final.ts"
