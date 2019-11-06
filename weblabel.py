#!/usr/bin/python

#import
import os #global
import time
from io import BytesIO
from flask import (  #web framework
    Flask,
    render_template,
    send_from_directory,
    send_file,
    request,
    redirect,
    url_for,
    request,
    session,
    Response,
    abort
)
from flask_sessionstore import Session #server side storage
import jinja2schema

from cairosvg import svg2png    #svg to bitmap
import re #regex for svg modification
from xml.dom import minidom #for svg modification
import PIL

from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

# config (todo)
'''
session['print_width']      = 384           # image = 384 x 175  -- print area =  384 x 154 
session['print_height']     = 154
session['print_spacing']    = 175-154
session['print_dpi']        = 171
'''

# app setup
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = os.urandom(24)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app) #server side storage config 


# return css static files
@app.route('/Semantic-UI-CSS/<path:path>')
def send_js(path):
    return send_from_directory('Semantic-UI-CSS', path)

# return a label svg template from collection 
@app.route('/svgtemplate/<path:path>')
def send_label(path):
    if path.startswith('recent'):
        cache_timeout = 1
    else:
        cache_timeout = 43200

    return send_from_directory('templates/labels', path, cache_timeout=cache_timeout)


# index page
@app.route('/')
def do_index():
   return redirect(url_for('do_choose')) #redirect to choose


# choose page
@app.route('/choose')
def do_choose():
    if 'labelsvg' in session:
        del session['labelsvg']

    labels = [f for f in os.listdir('templates/labels') if os.path.isfile(os.path.join('templates/labels/', f)) and f.endswith('.svg')] # get svg files
    labels.sort()
    return render_template('choose.html', labels = labels)

# select page

@app.route('/edit', methods=['GET'])
def do_edit():
    try:
        if 'labelsvg' in request.args:
            session['labelsvg'] = request.args['labelsvg']

        if 'labelsvg' in session:
            return render_edit()
        else:
            return redirect(url_for('do_choose')) #redirect to choose

    except Exception as e:
        raise
        print(str(e))
        return redirect(url_for('do_choose')) #redirect to choose


def load_fields():
    if 'fields' not in session:
        session['fields'] = {}

    session['fields'].update(request.form)


# preview page
@app.route('/preview', methods=['POST'])
def do_preview():
    load_fields()

    return render_edit()

def get_svg_dimensions(srcsvg):
    # the easiest/cleanest way to do it is just convert it to a PNG
    png_data = BytesIO()
    svg2png(bytestring=srcsvg, write_to=png_data)
    png = PIL.Image.open(png_data)

    return png.width, png.height

def svg_resize (srcsvg, target_width=696):
    width, height = get_svg_dimensions(srcsvg)

    scale = target_width / width
    new_height = height * scale

    tofile("resize_svg_src_debug.svg",srcsvg) #debug
    xmldoc = minidom.parseString(srcsvg)
    svg = xmldoc.getElementsByTagName("svg")[0]
    svg.setAttribute('width', str(target_width))
    svg.setAttribute('height', str(int(new_height)))


    dstsvg=xmldoc.toxml()

    tofile("resize_svg_dst_debug.svg",dstsvg) #debug

    return dstsvg

def render_edit():
    return render_template('edit.html', fields=get_label_template_vars())

def get_label_template_vars():
    with open("templates/labels/" + session['labelsvg']) as template_file:
        fields = list(sorted(jinja2schema.infer(template_file.read()).keys()))

    return fields

# return svg image
def render_svg():
    fields = session.get('fields', {})
    label_svg = session.get('labelsvg') or request.args.get('labelsvg', '')
    svg_data = render_template("labels/" + label_svg, **fields)
    svg_data = svg_resize(svg_data, 384) #resize svg image

    return svg_data


@app.route('/prev_img_svg')
def send_preview_img():
	#label template engine
    svg_data = render_svg()

    return Response(svg_data, mimetype='image/svg+xml')

# paper forward
@app.route('/forward', methods=['GET'])
def do_forward():
    try:
        nrpx = int(request.args['nrpx'])                        # read get param and convert to integer
        svg='<svg width="300" height="'+str(nrpx)+'"></svg>'    # create blank svg according to param
        svg_to_printer(svg) #sent to printer                    # print that svg
        return 'ok'
    except Exception as e:
        return 'error'

# print image
@app.route('/print', methods=["POST"])
def do_print():
    load_fields()
    svg_data = render_svg()
    save_recent(svg_data)
    result = svg_to_printer(svg_data)

    #print spacing :
    #svg='<svg width="300" height="'+str(21)+'"></svg>'    # create blank svg according to param
    #svg_to_printer(svg) #sent to printer                    # print that svg

    if result:
        return redirect(url_for('do_edit'))
    else:
        abort(500)


def svg_to_printer(svg):
     #config printer
    #   lsus
    #   lsusb -vvv -d 4b43:3538"b
    #   sudo usermod -a -G dialout user
    #   sudo usermod -a -G tty user
    #   sudo usermod -a -G lp user
    #   ls -la /dev/usb/

    # escape svg
    tofile("svg_to_print1_debug.svg",svg)
    #svg = svg.decode('utf-8').encode('ascii') # todo: problem with special char are used, find othern way to do that.
    tofile("svg_to_print2_debug.svg",svg)

    pngfile = BytesIO() #temp file
    png_data = svg2png(bytestring=svg, write_to=pngfile) #SVG to PNG

    for try_num in (1, 2, 3):
        try:
            printer = BrotherQLRaster('QL-800')
            printer.exception_on_warning = True
            instructions = convert(qlr=printer, cut=True, images=[pngfile], label="62", dither=True, dpi_600=False)
            send(instructions=instructions, printer_identifier='usb://0x04f9:0x209b/000A9Z276036', backend_identifier='pyusb', blocking=True)
        except Exception as exc:
            print("Error printing: %s (try %d)" % (str(exc), try_num))
            time.sleep(5)
        else:
            return True

    return False


def save_recent(svg_data):
    for i in range(9, 0, -1):
        from_file = "templates/labels/recent%d.svg" % i
        to_file = "templates/labels/recent%d.svg" % (i + 1)

        if os.path.exists(from_file):
            os.rename(from_file, to_file)

    tofile(from_file, svg_data)

def tofile(filename,content):
    text_file = open(filename, "w")
    text_file.write(content)
    text_file.close()
