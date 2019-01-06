> Sorry, I do my best, but English is not my mother tongue. Is there somebody helpfull for making text below more readable?

# WebLabel

You like labelling everything and with you ribbon printer Dymo or or Ptouch? But your are bored of being caught with overpriced proprietary supplies. If yes, grab your freedom with that project.

With almost dirty cheap ESC/POS compatible label printer and a raspbery pi, you now would be able to easily print your labels from web interafece.

Basically you will ,

1. Open web page from you smatphone or computer
2. Choose a template trought an SVG template collection (adresse, jam , note, on line text, two line texte, network, company logo ...) 
3. Enter custom text within an html form. 
   - texts are remplaced into selected SVG file with a template engine
4. Click print on preview windows
   - Your label is sent to your termal printer trought USB

**Note : at that time project is not yet fully fonctional (see roadmap below), but it it going to be usable soon.**

## Scrennshoot

- Choose template      [desktop](/doc/Choose.png)    [mobile](/doc/Choose_mobile.png)
- Edit text            [desktop](/doc/Edit.png)      [mobile](/doc/Edit_mobile.png)
- Preview+print        [desktop](/doc/Preview.png)   [mobile](/doc/Preview_mobile.png)

## Prerequisites
```
$ sudo apt-get install python
$ pip install Flask
$ pip install python-escpos
```

## Getting Started

1. Clone Gith hub respository.
2. Configure you printer usb port as below.
3. Download Semantic-UI-CSS into Semantic-UI-CSS sub folder.
5. Start web app with ./weblabel/run.sh
6. Open http://localhost:5000 within your favorite browser.


## Printer usb port setup

At the moment, you have to setup you printer manually.
That mean filling correponding value within weblabel.py : 

```
 p = Usb(0x4b43, 0x3538,0 ,0x82, 0x02  ) 
```

First and second value can be found with **lsusb** command before and after connection you printer.  
```
$ lsusb
...
Bus 002 Device 078: ID 18f8:0f97  
Bus 002 Device 077: ID 4b43:3538   <--that one 
Bus 002 Device 076: ID 05af:1012 Jing-Mold Enterprise Co., Ltd 
...
```

Third and last value can be found with :
```
lsusb -vvv -d 4b43:3538 |grep bEndpointAddress
        bEndpointAddress     0x02  EP 2 OUT
        bEndpointAddress     0x82  EP 2 IN
        
```

Also, be sure your user have access to usb port :
```
$ sudo usermod -a -G dialout user
$ sudo usermod -a -G tty user
$ sudo usermod -a -G lp user
```

## Road map

Work in progress :
- [x] Achieve function for replacing text within SVG, with jinja2 template engine.
- [x] Convert SVG into PNG according to printer print width resolution.
- [ ] Make a small advertising video

Short :
- [ ] Add a menu bare for advanced function and configuration.
- [ ] Buttons for manual paper alignement. That mean printing a blank image 1px(fine), 5px(normal) or 10px(large) height on button press.

Medium :
- [ ] Better label size managment. Actually it works, but label height and intervall are "hard coded" within SVG. template.
- [ ] Printer configuration page. Actually it works, but printer horizontal resolution is "hard coded".
- [ ] Label roll configuration page and drop down selection.
- [ ] SVG template création guideline.
- [ ] SVG upload page.

Long :
- [ ] Dynamic text input formulare according SVG File.
- [ ] Allow editing SVG template with a web SVG editor. (https://github.com/SVG-Edit/svgedit)

## Know issue

With inskape : flowed text won't show up on the internet. Convert back to regular text: Text menu > Convert to text. You might have to realign. Flowed text is created when you drag out a selection box before you type. To create regular text from the start, just click once and start typing. You can align/format afterwards using snapping and guides, if necessary.

## Authors

* **Rey Cyril** - *Initial work* - [cyrilrey](https://github.com/cyrilrey)

See also the list of [contributors](https://github.com/cyrilrey/weblabel/graphs/contributors) who participated in this project.

Help from people with opinions and common sens are welcome.


## License

This project is licensed under the GPL3 License - see the [LICENSE.md](LICENSE.md) file for details

## Tested with

GOOJPRT PT-210 from Aliexpress
Should work with almost all compatible POS thermal printer.

## Label paper

[Label 57*20mm](https://www.aliexpress.com/item/Direct-Thermal-Label-Stickers-10-Rolls-OD-40MM-Sutible-for-58mm-Bluetooth-Thermal-Labeller-Printer-57x40/32883774593.html?spm=a2g0s.9042311.0.0.27424c4dzTvZo8)

