@echo off
setlocal enabledelayedexpansion

:menu
cls
echo Musikplayer
echo -------------
echo.

set count=0
for %%f in (music\*.mp3) do (
    set /a count+=1
    set "file[!count!]=%%f"
    echo !count!. %%~nf
)

echo.
set /p choice="Waehlen Sie eine Nummer: "

if !choice! leq !count! (
    if !choice! gtr 0 (
        mkdir "%temp%\musicplayer" 2>nul
        echo !file[%choice%]!>"%temp%\musicplayer\current_song.txt"
        python musicplayer.py
    ) else (
        echo Ungueltige Auswahl
        pause
        goto menu
    )
) else (
    echo Ungueltige Auswahl
    pause
    goto menu
)
