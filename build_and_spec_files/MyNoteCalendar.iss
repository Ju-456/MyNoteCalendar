; MyNoteCalendar.iss

[Setup]
AppName=MyNoteCalendar
AppVersion=1.0
DefaultDirName={autopf}\MyNoteCalendar
DefaultGroupName=MyNoteCalendar
OutputDir=C:\Users\juuu4\Documents\MyNoteCalendar\installer
WizardStyle=modern
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\MyNoteCalendar.exe
SetupIconFile=C:\Users\juuu4\Documents\MyNoteCalendar\icon.ico  

[Files]
; Ton exécutable généré par PyInstaller
Source: "C:\Users\juuu4\Documents\MyNoteCalendar\dist\MyNoteCalendar.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Raccourci dans le menu démarrer
Name: "{group}\MyNoteCalendar"; Filename: "{app}\MyNoteCalendar.exe"; IconFilename: "{app}\MyNoteCalendar.exe"
; Raccourci sur le bureau
Name: "{commondesktop}\MyNoteCalendar"; Filename: "{app}\MyNoteCalendar.exe"; IconFilename: "{app}\MyNoteCalendar.exe"
