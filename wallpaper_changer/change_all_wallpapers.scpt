tell application "System Events"
	set desktopCount to count of desktops
	repeat with desktopNumber from 1 to desktopCount
		set rotinterval to change interval of desktop desktopNumber
		set change interval of desktop desktopNumber to rotinterval
	end repeat
end tell
