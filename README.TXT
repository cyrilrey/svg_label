# Project Title

You like labelling everything and with you ribbon printer Dymo or or Ptouch? If yes that project may interest you.

With a dirty cheap ESC/POS label printer and a raspbery pi, you now would be able to print from a web interafece.

Basically,
1) Open web page from you smatphone or computer
1) You choose a template trought an SVG collection (adresse, jam , note, on line text, two line texte, network, company logo ...) 
2) You enter custom text within an html form. 
	--> texts are remplaced into your SVG file with a template engine
3) You click print on preview windows
4) Label is sent to your termal printer trought USB


Note : at that time project is not yet fully fonctional , but it it going to soon.


## Prerequisites

python
pip install Flask
pip install python-escpos

## printer usb port setup

At the moment,you have to setup you printer manually.
That mean filling correponding value to that line within weblabel.py : 

'''
 p = Usb(0x4b43, 0x3538,0 ,0xB2, 0x02  )

'''

First and second value can be found with "lsusb" command before and after connection you printer.  
'''
$ lsusb
Bus 001 Device 002: ID 8087:8000 Intel Corp. 
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 003 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 002 Device 009: ID 0cf3:3004 Atheros Communications, Inc. AR3012 Bluetooth 4.0
Bus 002 Device 078: ID 18f8:0f97  
Bus 002 Device 077: ID 4b43:3538   <--that one 
Bus 002 Device 076: ID 05af:1012 Jing-Mold Enterprise Co., Ltd 
Bus 002 Device 075: ID 2001:f103 D-Link Corp. DUB-H7 7-port USB 2.0 hub
Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
'''

Third and last value can be found with "lsusb -vvv -d 4b43:3538"
'''
lsusb -vvv -d 4b43:3538 |grep EndpointAddress
'''

Allow usb access :
'''
sudo usermod -a -G dialout user
sudo usermod -a -G tty user
sudo usermod -a -G lp user
'''


## Getting Started

1) Clone Gith hub respository
2) configure you printer usb port as above
3) Download Semantic-UI-CSS into Semantic-UI-CSS sub folder
5) ./weblabel/run.sh
6) open http://localhost:5000 within your favorite browser


## Know issue

Flowed text won't show up on the internet. Convert back to regular text: Text menu > Convert to text. You might have to realign. Flowed text is created when you drag out a selection box before you type. To create regular text from the start, just click once and start typing. You can align/format afterwards using snapping and guides, if necessary.


## Authors

* **Rey Cyril** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GPL3 License - see the [LICENSE.md](LICENSE.md) file for details

## Tested with

GOOJPRT PT-210 from Aliexpress


## Label paper

Label 57*20 (https://www.aliexpress.com/item/Direct-Thermal-Label-Stickers-10-Rolls-OD-40MM-Sutible-for-58mm-Bluetooth-Thermal-Labeller-Printer-57x40/32883774593.html?spm=a2g0s.9042311.0.0.27424c4dzTvZo8)








#
