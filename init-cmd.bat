@ECHO OFF

SET CurrentDir=%~dp0
SET BinDir=%CurrentDir%bin

@ECHO.
@ECHO CurrentDir: "%CurrentDir%"
@ECHO BinDir    : "%BinDir%"
@ECHO.

SET PATH=%PATH%;"C:\Python27";"%BinDir%"

@ECHO %PATH%
@ECHO.

CALL cmd.exe