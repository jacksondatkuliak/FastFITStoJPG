# FastFITStoJPG

Quickly converts a single HDU in a FITS file into a jpg and saves it to disk.
Requires Python 3, I used Python 3.13.5.
Build by running "make all" or "make all_clean" if you would like make to automatically delete unnecessary files after compilation. Or, just use it with Python 3 if you have it installed. Does not require compilation.

Usage:
```
$ ./FastFITStoJPG -h
usage: FastFITStoJPG [-h] [--input INPUT] [--output OUTPUT] [--low LOW] [--high HIGH] [--stretch {linear,arcsinh,none}] [--boost BOOST] [--quality QUALITY] [--hdu HDU]

Convert FITS to JPEG with auto-stretching

options:
-h, --help show this help message and exit
--input INPUT Path to input FITS file (default input.fits)
--output OUTPUT Path to output JPEG file (default output.jpg)
--low LOW Low percentile for stretch (0-100, default: 0.5)
--high HIGH High percentile for stretch (0-100, default: 99.5)
--stretch {linear,arcsinh,none} Stretch mode: linear, arcsinh, or none (default linear)
--boost BOOST Arcsinh boost factor, only used if arcsinh stretch is selected (0-100, default 10)
--quality QUALITY JPEG quality (1-100, default: 80)
--hdu HDU FITS HDU to convert (-1-INT_MAX, default: -1 (last HDU))
```
Example jpeg converted from linear image
![converted jpg](https://github.com/jacksondatkuliak/FastFITStoJPG/blob/main/example.jpg "Example converted jpeg from linear image")
