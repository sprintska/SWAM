# SWAM
Star Wars Armada Modeler

This is a Monte Carlo simulation script built to model expected damage 
profiles in Star Wars Armada.  It's pretty rudimentary--like, it's in 
alpha and will probably never leave it.  If you don't know Python, you 
should only change the variables under OPTIONS.  To add the effect of 
an upgrade, set the variable equal to 1; to remove it, set it to 0. The 
color_base variables set the number of dice in the pool.

To run this script, make sure you have Python 3 installed, then type 
$ py path/to/script/py montecarlo.py on the command line.  It was written 
and tested for Python 3.4.  If you have Python 2, go get the current 
version, weiner.  If you have a newer version, hello from the past!

---------------------
WINDOWS
---------------------
-Setup:

1. Download and install the latest version of Python 3 from here:
https://www.python.org/downloads/windows/

2. Put all of the SWAM files into any directory on your computer.  I'll 
use C:\path\to\script\ for the instructions.

-Use:

1. Type Window-R to bring up the run dialog, or open it from the Start 
menu, and type cmd.exe.  This will bring you to the command line.

2. At the command prompt (which will look something like 
C:\FolderName>), type:
py C:\path\to\script\montecarlo.py

3. To change options, you currently need to edit the script directly.  
To do this, open C:\path\to\script\montecarlo.py in Notepad and follow 
the directions at the top of the file.

---------------------
LINUX
---------------------
-Setup

1. $ sudo apt-get install python

2. Put all of the SWAM files into any directory on your computer.  I'll 
use /path/to/script/ for the instructions

3. $ chmod +x /path/to/script/montecarlo.py

-Use:

1. $ /path/to/script/montecarlo.py 

2. To change options, you currently need to edit the script directly.  
To do this, open \path\to\script\montecarlo.py in nano or your favorite 
text editor and follow the directions at the top of the file.

---------------------
MAC
---------------------
-Setup

1. Install Linux

2. Follow Linux instructions
