* **Can I contribute to the project?**\
Absolutely! Feel free to submit pull requests, issues or to write directly to me(Telegram) if you want to help the project.

* **Why is the installation process so intricated?**\
Because it's the first time I create a project meant to be usable. I will improve it soon.

* **The software doesn't work and I see no logging file in the /var/log/onaccessvt directory**\
Logging is currently not implemented in a perfect way so feel free to contact me on Telegram and I will try to help you directly.

* **Why the software has two components?**\
I was trying to learn fanotify kernel API so I started writing down a program in C.\
Then I realised that handling the HTTP request would be a pain in C so I decided to write in python the request handler without throwing away my C code.\
This choice made possible the standalone usage of the two components, maybe in future I will rewrite everything in C++ and make one single binary file.
