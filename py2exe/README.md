pyinstaller --onefile --add-data "configlogin.yaml;." screenshot_uploader.py

```wxs
<?xml version="1.0"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="ScreenshotUploader" Language="1033" Version="1.0.0.0" Manufacturer="YourCompany" UpgradeCode="5577f0f1-a2a3-45ad-a095-a02b32f0602b">
    <Package InstallerVersion="200" Compressed="yes" InstallScope="perMachine" />

    <Media Id="1" Cabinet="media1.cab" EmbedCab="yes" />

    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="ScreenshotUploader" />
      </Directory>
    </Directory>

    <!-- Added Directory attribute to specify where the component will be installed -->
    <Component Id="ProductComponent" Directory="INSTALLFOLDER" Guid="5577f0f1-a2a3-45ad-a095-a02b32f0602b">
      <File Id="screenshot_uploader.exe" Source="/home/bol7/wix_project/screenshot_uploader.exe" KeyPath="yes" />
    </Component>

    <Feature Id="ProductFeature" Title="ScreenshotUploader" Level="1">
      <ComponentRef Id="ProductComponent" />
    </Feature>
  </Product>
</Wix>
```
