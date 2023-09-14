# OnAccess VirusTotal Scanner
OnAccess VirusTotal Scanner (OnAccessVT shortened) is a software, designed for linux, that scans files created in specified directories using VirusTotal engine.
The tool does not yet supports file uploading so it makes a requests to VirusTotal API with the file HASH and retrieve the answer displaying it to the user.

** Software is currently tested and working on Ubuntu 22.04 and 23.04, not guaranteed it works on other environments **

## Requirements
  * VirusTotal Account with a API-KEY, currently free with some limitations: [VT Public API limitations](https://developers.virustotal.com/reference/public-vs-premium-api)
  * Linux kernel version >= 5.9
  * Linux kernel fanotify API enabled
  * vt-py (Installed during setup, is the official VirusTotal API library for Python3)
  * python3-tk (Installed during setup, is a GUI library for Python3)
  * gcc (Usually pre-installed with OS, is a compiler for C language)
  * notify-send (Usually pre-installed with OS, is a tool used to send notifications to the user)

## Requirements check
