### NOTE: This file is not a part of web applicaton, to be used on the client machine to workaround the network access limitations of pythonanywhere
### SET FOLDER TO WATCH + FILES TO WATCH + SUBFOLDERS YES/NO
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "C:\Users\krish\Downloads"
$watcher.Filter = "*.csv"
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true  
$global:uploadUriSettle = "http://127.0.0.1:8000/api/posist/"
$global:curlExecLocation = "C:\Git\mingw64\bin\curl"
$global:fileNamePattern = "Daily_Sales_Summary.*Jubilee Hills"

### DEFINE ACTIONS AFTER AN EVENT IS DETECTED
$action = { 
    $fileName = $Event.SourceEventArgs.Name
    $changeType = $Event.SourceEventArgs.ChangeType
    $path = $Event.SourceEventArgs.FullPath
    if (($fileName -match $fileNamePattern) -and ($changeType -eq 'Renamed') -and ((Get-Item $path).length) -gt 1kb) {
        $logline = "$(Get-Date -format 'yyyy-MM-dd HH:mm:ss'), $changeType, $path, $fileName"
        Add-content "$PSScriptRoot\PushCSV.log" -value $logline
        $curl_cmd = "$curlExecLocation --location --request POST '$uploadUriSettle' --header 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' -F 'file=@$path'"
        # Add-content "$PSScriptRoot\PushCSVLog.txt" -value $curl_cmd
        Invoke-Expression $curl_cmd
    }
}    
### DECIDE WHICH EVENTS SHOULD BE WATCHED 
# Register-ObjectEvent $watcher "Created" -Action $action
# Register-ObjectEvent $watcher "Changed" -Action $action
# Register-ObjectEvent $watcher "Deleted" -Action $action
# using rename watcher because the chrome downloads as .crdownload first and renames to actual after download complete
Register-ObjectEvent $watcher "Renamed" -Action $action
while ($true) { Start-Sleep 5 }