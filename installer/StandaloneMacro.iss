#define MyAppName "Standalone Macro Studio"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Standalone Macro"
#define MyAppExeName "StandaloneMacro.exe"

[Setup]
AppId={{DAB17E92-9B10-4B2C-90EB-FF0EE815D112}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\StandaloneMacroStudio
DefaultGroupName=Standalone Macro Studio
OutputDir=output
OutputBaseFilename=StandaloneMacroSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Maak een bureaublad-snelkoppeling"; GroupDescription: "Extra taken:"; Flags: unchecked

[Files]
Source: "..\dist\StandaloneMacro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Standalone Macro Studio"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Standalone Macro Studio"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Start Standalone Macro Studio"; Flags: nowait postinstall skipifsilent
