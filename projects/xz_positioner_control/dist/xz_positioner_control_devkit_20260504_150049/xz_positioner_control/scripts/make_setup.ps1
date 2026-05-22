param(
  [string]$ProjectRoot = "C:\Users\mzeray\Documents\Web-Automation-V2\projects\xz_positioner_control"
)

$ErrorActionPreference = "Stop"
$iss = Join-Path $ProjectRoot "scripts\installer.iss"

@"
[Setup]
AppName=XZ Positioner Control UI
AppVersion=0.1.0
DefaultDirName={autopf}\XZControlUI
DefaultGroupName=XZControlUI
OutputDir=$ProjectRoot\dist
OutputBaseFilename=XZControlUI_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "$ProjectRoot\dist\XZControlUI\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\XZ Control UI"; Filename: "{app}\XZControlUI.exe"
Name: "{commondesktop}\XZ Control UI"; Filename: "{app}\XZControlUI.exe"
"@ | Set-Content -LiteralPath $iss -Encoding UTF8

$iscc = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if (Test-Path $iscc) {
  & $iscc $iss
  Write-Host "setup.exe created under dist\XZControlUI_Setup.exe"
} else {
  Write-Host "Inno Setup not found. Install Inno Setup 6 then rerun this script."
}
