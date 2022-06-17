# Craplog pyGUI
Parse Apache2 logs to create statistics

<br/>

## Overview

Craplog is a tool that takes Apache2 logs in their default form, scrapes them and creates simple statistics.<br/>
It's meant to be ran daily.

![screenshot](https://github.com/elB4RTO/craplog-pyGUI/blob/main/crapshot.png)<br/>

In the left side of the screen, you can load and view the log files that will be used.<br/>
In the right side of the screen, there are the options to use and the output of the process.

<br/>

Don't like the GUI? Try the [other versions of Craplog](https://github.com/elB4RTO/CRAPLOG#official-versions)

<br/>

## Dependencies
- ***tk***   ( *tkinter* )

<br/>

## Usage with installation

```
chmod +x install.sh
./install.sh
craplog
```

<br/>

## Usage without installation
```
python3 ./craplog.py
```

<br/><br/>

## Important note

Unlike the previous versions, this version will **automatically remove confilct files** during execution.<br/>
Don't store personal stuff inside Craplog's folder.

<br/>

## Log files

At the moment, it only supports **Apache2** log files in their **default** form and path.<br/>
If you're using a different path, please open the file named **Clean.py** (you can find it inside the folder named *crappy*) and **modify** these lines:
- [7](https://github.com/elB4RTO/craplog-pyGUI/blob/main/craplog/crappy/Clean.py#L7)  **]** for the *access.log.1* file
- [67](https://github.com/elB4RTO/craplog-pyGUI/blob/main/craplog/crappy/Clean.py#L67) **]** for the *error.log.1* file

<br/>

## Default path

/var/log/apache2/

<br/>

## Default logs form

### access.log.1
  
IP - - [DATE:TIME] "REQUEST URI" RESPONSE "FROM URL" "USER AGENT"<br/>
*123.123.123.123 - - [01/01/2000:00:10:20 +0000] "GET /style.css HTTP/1.1" 200 321 "/index.php" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Firefox/86.0"*<br/><br/>

### error.log.1

[DATE TIME] [LOG LEVEL] [PID] ERROR REPORT<br/>
*[Mon Jan 01 10:20:30.456789 2000] [headers:trace2] [pid 12345] mod_headers.c(874): AH01502: headers: ap_headers_output_filter()*

<br/>

#### Note
Please notice that Craplog is taking **.log.1** files as input. This is because these files (by default) are renewed every day at midnight, so they contain the full log stack of the (past) day.<br/>
Because of that, when you run it, it will use yesterday's logs and store stat files cosequently.<br/>
Craplog is meant to be ran daily.

<br/>

## Cleaned access logs file

This is nothing special. It just creates a file in which every line from a local connection is removed (this happens with statistics too).<br/>
After that, the lines are re-arranged in order to be separeted by one empty line if the connection comes from the same IP address as the previous, or two empty lines if the IP is different from the above one.<br/>
This isn't much useful if you usually check logs using *cat | grep*, but it helps if you read them directly from file.<br/>
Not a default feature.

<br/>

## Single-session statistics

By default, Craplog takes as input only the ***access.log.1*** file (unless you specify to not use it, calling the `only errors` argument, see below).

The first time you run it, it will create a folder named *STATS*.<br/>
Stattistics files will be stored inside that folder and sorted by date.<br/><br/>

Four **.crapstats** files will be created inside the folder named *STATS*:
- **IP**.*crapstats* = IPs statistics of the choosen file
- **REQ**.*crapstats* = REQUESTs statistics of the choosen file
- **RES**.*crapstats* = RESPONSEs statistics of the choosen file
- **UA**.*crapstats* = USER AGENTs statistics of the choosen file<br/><br/>

You have the opportunity to also create statistics of the **errors** ( `errors` ) or even of the errors only ( `only errors` , avoiding the usage of the access.log.1 file).

This will create 2 additional files inside STATS folder:
- **LEV**.*crapstats* = LOG LEVELs statistics of the choosen file
- **ERR**.*crapstats* = ERROR REPORTs statistics of the choosen file

<br/>

## Global statistics

Additionally, by default Craplog updates the **global** statistics inside the *STATS/GLOBALS* folder every time you run it (unless you specify to not do it, calling `avoid globals` ).

Please notice that if you run it twice for the same log file, GLOBAL statistics will not be reliable (obviously).<br/><br/>

A maximum of 6 files will be created inside *STATS/GLOBALS/*:
- **GLOBAL.IP**.*crapstats* = GLOBAL IPs statistics
- **GLOBAL.REQ**.*crapstats* = GLOBAL REQUESTs statistics
- **GLOBAL.RES**.*crapstats* = GLOBAL RESPONSEs statistics
- **GLOBAL.UA**.*crapstats* = GLOBAL USER AGENTs statistics
<br/><br/>*[**+**]*<br/><br/>
- **GLOBAL.LEV**.*crapstats* = GLOBAL LOG LEVELs statistics
- **GLOBAL.ERR**.*rapstats* = GLOBAL ERROR REPORTs statistics

<br/>

## Statistics structure

Statistics' structure is the same for both **sessions** and **globals**:

{ ***COUNT*** } &emsp; >>> &emsp; ***ELEMENT***<br/><br/>

*example*:

{ 100 } &emsp; >>> &emsp; 200<br/>
{ 10 } &emsp; >>> &emsp; 404

<br/>

## Usage examples


- Craplog's complete functionalities: makes a clean access logs file, creates statisics of both *access.log.1* and *error.log.1* files, uses them to update globals and creates a backup of the original files

  `clean` `errors` `backup`<br/><br/>


- Takes both access logs and error logs files as input, but only updates global statistics. Move conflict files to trash instead of delete

  `errors` `only globals` `trash`<br/><br/>


- Also creates statisics of error logs file, but avoids updating globals

  `errors` `avoid globals`

<br/>

#### Note
Please notice that even usign `only globals`, normal session's statistic files will be created. Craplog needs session files in order to update global ones.<br/>
After completing the job, session files will be automatically removed.

<br/>

## Final considerations

#### Estimated working speed

1~10 MB/s

May be higher or lower depending on the complexity of the *logs*, the length of your *globals* and the power of your CPU.<br/>
If it takes more than 1 minute for a 10 MB file, you've probably been tested in some way (better to check).<br/><br/>

#### Global's backups

Craplog automatically makes backups of global statistics files, in case of fire.<br/>
If something goes wrong and you lose your actual global files, you can recover them (at least the last backup).<br/>
Move inside Craplog's folder, open '**STATS**', open '**GLOBALS**', show hidden files and open '**.BACKUPS**'. Here you will find the last 7 backups taken.<br/>
Folder named '7' is always the newest and '1' the oldest.<br/>
A new backup is made every 7th time you run Craplog. If you run it once a day, it will takes backups once a week, and will keep the older one for 7 weeks.<br/><br/>

#### Developement and contribution

Craplog is under development.<br/>
If you have suggestions about how to improve it please open an issue.<br/><br/>

If you're not running Apache, but you like this tool: same as before, comment (bring a sample of a log file).

<br/>
