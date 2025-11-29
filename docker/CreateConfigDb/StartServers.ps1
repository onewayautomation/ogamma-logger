$numberOfServers=50
$defaultConfig = [IO.File]::ReadAllText($PSScriptRoot+"/ServerConfig.xml")

for ($port=48010; $port -le (48010+$numberOfServers); $port++) {
	$configFileName = $PSScriptRoot+"/ServerConfig"+$port.ToString()+".xml"
	$thisServerConfig = $defaultConfig -replace "48010", $port.ToString()
	$thisServerConfig | Out-File $configFileName
	$argList="-c "+ $configFileName 
	Start-Process "C:/Program Files (x86)/UnifiedAutomation/UaCPPServer/bin/uaservercpp.exe" -ArgumentList "$argList"
}
