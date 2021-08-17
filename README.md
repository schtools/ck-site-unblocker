### UPDATE
I will be releasing the source code and explanation on how I made this soon when I finish implementing a couple features so anyone can adapt my code and create any system they want with it. 
These features will include:
- ~~Being able to change which of the three requests are sent to the appliance (more information to come when I open source it)~~ **Completed**
- Checking whether the requests actually worked by reading the response HTML rather than simply checking the status code **Will be completed within the next week**
- ~~Being able to change the default classification (default is technology/29 which guarentees an unblock on most sites)~~ **Completed**
# Contentkeeper Site Unblocker
This is a portable application that allows you to essentially "unblock" nearly any URL. **Source code will be unavaliable for the forseeable future (most likely until the end of 2022) as to not allow the exploit to be patched.** This requires that your network has the "Contentkeeper Appliance" on it. I am unsure if this will work on every Contentkeeper system as I only designed it for the one I am used to. I have heard of different institutions installing the blocking software directly onto computers, so I am unsure if this program will work with those setups.

The program also has a form of "DRM" in it which prevents it from running if it doesn't recieve a specific response from a site. This was implemented so I could control access, however you can feel free to remove it when I eventually make it open source. If you try run the exe and you get a message saying I have disabled the program, this means one of three things:
1) Github is down/blocked (I can't do anything about this)
2) The program can't access the verification file for one reason or another
3) I have disabled access to the program temporarily.
In most cases, it would probably be option 3. I'll only disable access to the program if something bad happens with it IRL.

If the program ever crashes, feel free to create an issue in the issues tab with the traceback.txt and description on how the error occured.
### Installing
Simply download the latest version from the releases tab and run it like a normal executable. Windows will probably think it's a virus due to the way it was compiled. I can assure you that it is not a virus, however you can decide whether you would trust me or not.
### Credits
Iconarchive.com for the icon: https://iconarchive.com/show/polygon-icons-by-graphicloads/lock-unlock-icon.html (I'm not actually sure if I can use their icon with this).
My institution for providing the motivation to make this.
Contentkeeper for providing my institution with your system and the "vulnerability" allowing me to do this (I doubt my method could be considered a system vulnerability).
### Note
I am not responsible for any trouble I may get anyone into if they choose to use this tool, this is on you pal. Furthermore this tool is for educational use only, don't use it maliciously!!!
If you are to fork this repo and create your own version, remember to credit me in the code and gui. Also DO NOT ADD MALICIOUS CODE WHATSOEVER!
