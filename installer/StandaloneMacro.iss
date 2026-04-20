#define MyAppName "Standalone Macro Studio"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Standalone Macro"
#define MyAppExeName "StandaloneMacro.exe"

[Setup]
AppId={{DAB17E92-9B10-4B2C-90EB-FF0EE815D112}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=https://example.com
AppSupportURL=https://example.com
AppUpdatesURL=https://example.com
DefaultDirName={autopf}\StandaloneMacroStudio
DefaultGroupName=Standalone Macro Studio
OutputDir=output
OutputBaseFilename=StandaloneMacroSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
UninstallDisplayIcon={app}\{#MyAppExeName}
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Installer for Standalone Macro Studio
DisableProgramGroupPage=yes
; Voor later: ondertekenen via Inno Setup (voorbeeld)
; SignTool=signtool sign /fd SHA256 /f "C:\certs\codesign.pfx" /p "{#CodeSignPassword}" $f
; SignedUninstaller=yes

#ifexist "..\assets\app.ico"
SetupIconFile=..\assets\app.ico
#endif

[Languages]
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Maak een bureaublad-snelkoppeling"; GroupDescription: "Extra taken:"; Flags: unchecked

[Files]
Source: "..\dist\StandaloneMacro.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Standalone Macro Studio"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Standalone Macro Studio"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Start Standalone Macro Studio"; Flags: nowait postinstall skipifsilent
