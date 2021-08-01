@if (@X)==(@Y) @end /* JScript comment
@echo off

setlocal
del /q /f %~n0.exe >nul 2>&1
for /f "tokens=* delims=" %%v in ('dir /b /s /a:-d  /o:-n "%SystemRoot%\Microsoft.NET\Framework\*jsc.exe"') do (
   set "jsc=%%v"
)

if not exist "%~n0.exe" (
    "%jsc%" /nologo /out:"%~n0.exe" "%~dpsfnx0"
)

if exist "%~n0.exe" ( 
    "%~n0.exe" %* 
)


endlocal & exit /b %errorlevel%

end of jscript comment*/

import System;
import System.Windows;
import System.Windows.Forms;
import System.Drawing;
import System.Drawing.SystemIcons;

var notification;
try {
    notification = new System.Windows.Forms.NotifyIcon();


} catch (err){

}

notification.Icon = System.Drawing.SystemIcons.Hand; // Could be Application,Asterisk,Error,Exclamation,Hand,Information,Question,Shield,Warning,WinLogo
notification.BalloonTipText = "Qbot turned off!!";
notification.Visible = true;
notification.BalloonTipTitle = "Qbot"
notification.BalloonTipIcon = System.Windows.Forms.ToolTipIcon.Info
// optional - BalloonTipIcon = System.Windows.Forms.ToolTipIcon.Info;
// optional - BalloonTipTitle = "Qbot",




// Display for 2 seconds.
notification.ShowBalloonTip(2000);
System.Threading.Thread.Sleep(2100);

notification.Dispose();