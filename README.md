# craplog-fullGUI
A tool that scrapes Apache2 logs to create both Single-Session and Global statistics

/<br>
<br>
CRAPLOG is a tool that takes Apache2 logs in their default form, scrapes them and creates simple statistics.<br>
It's meant to be ran daily.<br>
<br>
<br>
<img src="https://github.com/elB4RTO/CRAPLOG/blob/main/crapshots/full_GUI.png">
<br>
<br>
This fully Graphical version of CRAPLOG allows you to view log files too.<br>
In the left side of the screen, you can load and view the files that CRAPLOG will use during its job.<br>
In the right side of the screen, there are the options to use and the output of the process.<br><br>
Don't like the GUI? Try the <a href="https://github.com/elB4RTO/craplog-fullCLI">full CLI</a> or the <a href="https://github.com/elB4RTO/craplog-GUIaidedCLI">GUI aided CLI</a> versions<br>
<br>
<br>
<br>
<b>DEPENDENCIES</b>:<br>
- <i><b>tk</b></i>   ( <i>tkinter</i> )<br>

<b>OTHER DEPENDENCIES</b>:<br>
- <i>os</i>, <i>sys</i>, <i>time</i>, <i>pathlib</i>, <i>datetime</i>, <i>subprocess</i>, <i>collections</i>
<br>
<br>
<br>
<b>USAGE WITH INSTALLATION</b>:<br>
<br>
<code>chmod +x ./install.sh</code><br>
<code>exec ./install.sh</code><br>
<code>craplog</code><br>
<br>
<br>
<br>
<b>USAGE WITHOUT INSTALLATION</b>:<br>
<br>
<code>chmod +x ./craplog.py ./crappy/*.py</code><br>
<code>./craplog.py</code><br>
<br>
<br><hr><br>
<br>
<b>IMPORTANT NOTE</b>:<br>
<br>
Unlike the previous versions, this version of CRAPLOG will <b>automatically remove confilct files</b> during execution<br>
<br>
<br><hr><br>
<br>
<b>LOG FILES</b>:<br>
<br>
At the moment, it only supports <b>Apache2</b> log files in their <b>default</b> form and path<br>
If you're using a different path, please open the file named <b>Clean.py</b> (you can find it inside the folder named <i>crappy</i>) and <b>modify</b> these lines:<br>
- <b>7</b> ] for the <i>access.log.1</i> file<br>
- <b>67</b> ] for the <i>error.log.1</i> file<br>
<br>
<br>
<i>DEFAULT PATH:</i><br>
<br>
/var/log/apache2/<br>
<br>
<br>
<i>DEFAULT LOG FORMS:</i><br>
<br>
<b>access.log.1</b><br>
IP - - [DATE:TIME] "REQUEST URI" RESPONSE "FROM URL" "USER AGENT"<br>
123.123.123.123 - - [01/01/2000:00:10:20 +0000] "GET /style.css HTTP/1.1" 200 321 "/index.php" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Firefox/86.0"<br>
<br>
<b>error.log.1</b><br>
[DATE TIME] [LOG LEVEL] [PID] ERROR REPORT<br>
[Mon Jan 01 10:20:30.456789 2000] [headers:trace2] [pid 12345] mod_headers.c(874): AH01502: headers: ap_headers_output_filter()<br>
<br>
<br>
<i>NOTE</i>:<br>
Please notice that CRAPLOG is taking <b>*.log.1</b> files as input. This is because these files (by default) are renewed every day at midnight, so they contain the full log stack of the (past) day.<br>
Because of that, when you run it, it will use yesterday's logs and store stat files cosequently.<br>
CRAPLOG is meant to be ran daily.<br>
<br>
<br><hr><br>
<br>
<b>CLEAN.access.log FILE</b>:<br>
<br>
This is nothing special. It just creates a file in which every line from a local connection is removed (this happens with statistics too).<br>
After that, the lines are re-arranged in order to be separeted by one empty line if the connection comes from the same IP address as the previous, or two empty lines if the IP is different from the above one.<br>
This isn't much useful if you usually check logs using <i>cat | grep</i>, but it helps if you read them directly from file.<br>
Not a default feature.<br>
<br>
<br>
<br>
<b>SINGLE-SESSION STATISTIC FILES</b>:<br>
<br>
By default, CRAPLOG takes as input only the <b><i>access.log.1</i></b> file (unless you specify to not use it, calling the <i>--only-errors</i> argument, see below).<br>
<br>
The first time you run it, it will create a folder named <i>STATS</i>.<br>
Stat files will be stored inside that folder and sorted by date.<br>
<br>
Four <i>*.crapstats</i> files will be created inside the folder named STATS:<br>
- <b>IP.crapstats</b> = IPs statistics of the choosen file<br>
- <b>REQ.crapstats</b> = REQUESTs statistics of the choosen file<br>
- <b>RES.crapstats</b> = RESPONSEs statistics of the choosen file<br>
- <b>UA.crapstats</b> = USER AGENTs statistics of the choosen file<br>
<br>
You have the opportunity to also create statistics of the errors (<i>--errors</i>) or even of only the errors (<i>--only-errors</i> , avoiding the usage of the access.log.1 file).<br>
This will create 2 additional files inside STATS folder:<br>
- <b>LEV.crapstats</b> = LOG LEVELs statistics of the choosen file<br>
- <b>ERR.crapstats</b> = ERROR REPORTs statistics of the choosen file<br>
<br>
<br>
<br>
<b>GLOBAL STATISTIC FILES</b>:<br>
<br>
Additionally, by default CRAPLOG updates the GLOBAL statistics inside the <i>/STATS/GLOBALS</i> folder every time you run it (unless you specify to not do it, calling <i>--avoid-globals</i>).<br>
<br>
Please notice that if you run it twice for the same log file, GLOBAL statistics will not be reliable (obviously).<br>
<br>
A maximum of 6 GLOBAL files will be created inside craplog/GLOBALS/:<br>
- <b>GLOBAL.IP.crapstats</b> = GLOBAL IPs statistics<br>
- <b>GLOBAL.REQ.crapstats</b> = GLOBAL REQUESTs statistics<br>
- <b>GLOBAL.RES.crapstats</b> = GLOBAL RESPONSEs statistics<br>
- <b>GLOBAL.UA.crapstats</b> = GLOBAL USER AGENTs statistics<br>
[+]<br>
- <b>GLOBAL.LEV.crapstats</b> = GLOBAL LOG LEVELs statistics<br>
- <b>GLOBAL.ERR.crapstats</b> = GLOBAL ERROR REPORTs statistics<br>
<br>
<br><hr><br>
<br>
<b>STATISTICS STRUCTURE</b>:<br>
<br>
Statistics' structure is the same for both SESSION and GLOBALS:<br>
<br>
<b>{ </b><i>COUNT</i><b> } &emsp; >>> &emsp; </b><i>ELEMENT</i><br>
<br>
<br>
<i>example</i>:<br>
<br>
{ 100 } &emsp; >>> &emsp; 200<br>
{ 10 } &emsp; >>> &emsp; 404<br>
<br>
<br><hr><br>
<br>
<b>USAGE EXAMPLES</b>:<br>
<br>
<i>- CRAPLOG's complete functionalities: makes a clean access logs file, creates statisics of both access.log.1 and error.log.1 files, uses them to update globals and creates a backup of the original files</i><br>
<code>clean</code> <code>errors</code> <code>backup</code><br>
<br>
<i>- Takes both access logs and error logs files as input, but only updates global statistics. Move conflict files to trash instead of delete</i><br>
<code>errors</code> <code>only globals</code> <code>trash</code><br>
<br>
<i>- Also creates statisics of error logs file, but avoids updating globals</i><br>
<code>errors</code> <code>avoid globals</code><br>
<br>
<br>
<b>PS</b>:<br>
Please notice that even usign <code>only globals</code>, normal SESSION's statistic files will be created. CRAPLOG needs session files in order to update global ones.<br>
After completing the job, session files will be automatically removed.<br>
<br>
<br><hr><br>
<br>
<b>FINAL CONSIDERATIONS</b>:<br>
<br>
ESTIMATED WORKING SPEED:<br>
1~10 sec / 1 MB<br>
<br>
May be higher or lower depending on the complexity of your SESSION logs, the length of your GLOBALS and the power of your CPU.<br>
If CRAPLOG takes more than 1 minute for a 10 MB file, you've probably been tested in some way (better to check).<br>
<br>
<br>
CRAPLOG automatically makes backups of GLOBAL statistic files, in case of fire.<br>
If something goes wrong and you lose your actual GLOBAL files, you can recover them (at least the last backup).<br>
Move inside CRAPLOG folder, open 'STATS', open 'GLOBALS', show hidden files and open '.BACKUPS'. Here you will find the last 7 backups taken.<br>
Folder named '7' is always the newest and '1' the oldest.<br>
A new BACKUP is made every 7th time you run CRAPLOG. If you run it once a day, it will takes backups once a week, and will keep the older one for 7 weeks.<br>
<br>
CRAPLOG is under development.<br>
If you have suggestions about how to improve it please comment.<br>
<br>
If you're not running Apache, but you like this tool: same as before, comment (bring a sample of a log file).<br>
