; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{AAB640BD-F226-483A-B02B-B626F9D91A24}
AppName=���-������ �����������
AppVersion=0.99
;AppVerName=���-������ "���������" 1.0
AppPublisher=���1-15-1�
AppPublisherURL=http://web-service-test.cloudapp.net
OutputDir=win_installer
OutputBaseFilename=ProjectMSF-Windows
PrivilegesRequired=lowest
DefaultDirName={localappdata}\���-������ ���������
DefaultGroupName=���-������ �����������
DisableProgramGroupPage=yes
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\server\server.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "�������.pdf"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "dist\server\*"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\server\data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\server\client\*"; DestDir: "{app}\client"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\���-������ �����������"; Filename: "{app}\server.exe"; Parameters: "-e client"; Comment: "��������� ���-������"
Name: "{group}\������������"; Filename: "{app}\�������.pdf"; Comment: "������� ���� ���������� ������������"
Name: "{commondesktop}\���-������ �����������"; Filename: "{app}\server.exe"; Tasks: desktopicon; Parameters: "-e client"


[Run]
Filename: "{app}\server.exe"; Description: "{cm:LaunchProgram,���-������ �����������}"; Flags: nowait postinstall skipifsilent; Parameters: "-e client"

