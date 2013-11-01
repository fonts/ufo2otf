#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import mkdir
from os.path import splitext, dirname, sep, join, exists, basename
from subprocess import Popen
from diagnostics import diagnostics, known_compilers, FontError
import codecs
import re

diagnostics = diagnostics()

class Compiler:
    def __init__(self,infiles,webfonts=False,afdko=False):
        # we strip trailing slashes from ufo names,
        # otherwise we get confused later on when
        # generating filenames:
        self.infiles = [i.strip(sep) for i in infiles]
        self.webfonts = webfonts
        self.css = ''

        if afdko:
            if diagnostics['afdko']:
                self.compile = self.afdko
            else:
                raise FontError("afdko", diagnostics)
        else:
            if diagnostics['fontforge']:
                self.compile = self.fontforge
            else:
                raise FontError("fontforge", diagnostics)

    def fontforge(self):
        import fontforge
        
        eot = False
        if diagnostics['mkeot']:
            eot = True
        
        for infile in self.infiles:
            outdir = dirname(infile)
            name = splitext(infile)[0]
            font = fontforge.open(infile)
            otf_file_name = join(outdir, basename(name) + '.otf')
            if splitext(infile)[1].lower != 'otf':
                """
                Even if the tool is called Ufo2Otf, it can be used on otf’s too:
                In that case it’s just to generate webfonts. If an otf file is the
                infile, we skip otf generation.
                """
                font.generate(otf_file_name, flags=("round"))
            
            if self.webfonts:
                # Optimise for Web
                font.autoHint()
                
                # Generate Webfonts
                webfonts_path = join(outdir, 'webfonts')
                if not exists(webfonts_path):
                    mkdir(webfonts_path)
                    
                woff_file_name = join(outdir, 'webfonts', basename(name) + '.woff')
                ttf_file_name = join(outdir, 'webfonts', basename(name) + '.ttf')
                eot_file_name = join(outdir, 'webfonts', basename(name) + '.eot')

                font.generate(woff_file_name, flags=("round"))
                font.generate(ttf_file_name, flags=("round"))
                if eot:
                    eot_file = open(eot_file_name, 'wb')
                    pipe = Popen(['mkeot', ttf_file_name], stdout=eot_file)
                    pipe.wait()
                
                # Generating CSS
                #
                # CSS can only cover a limited set of styles:
                # it knows about font weight, and about the difference between
                # regular and italic.
                # It also knows font-style: oblique, but most browser will take
                # the regular variant and slant it.
                font_style = "normal"
                # This tends to work quite well, as long as you have one kind of
                # italic in your font family:
                if font.italicangle != 0:
                    font_style = "italic"
                
                # CSS weights map quite well to Opentype, so including families
                # with lots of different weights is no problem.
                #
                # http://www.microsoft.com/typography/otspec/os2ver0.htm#wtc
                # ->
                # http://www.w3.org/TR/CSS21/fonts.html#font-boldness
                font_weight = font.os2_weight
                #
                # Anything else, like condensed, for example, will need to be 
                # be put into a different font family, because there is no way
                # to encode it into CSS.
                #
                # What we do here, is try to determine whether this is the case.
                # ie:
                # >>> font.fullname
                # 'Nimbus Sans L Bold Condensed Italic'
                # >>> font.familyname
                # 'Nimbus Sans L'
                # >>> font.weight
                # 'Bold'
                # >>> re.findall("italic|oblique", f.fullname, re.I)
                # ['Italic']
                #
                # By then removing all these components from the full name,
                # we find out there is a specific style such as, in this case,
                # 'Condensed'
                font_family = font.familyname
                specifics = re.sub("italic|oblique", '',
                   font.fullname.
                   replace(font.familyname, '').
                   replace(font.weight, ''),
                flags=re.I).strip()
                if specifics:
                    font_family = "%s %s" % (font.familyname, specifics)
                
                if eot:
                    self.css += """@font-face {
    font-family: '%s';
    font-style: '%s';
    font-weight: '%s';
    src: url('%s'); /* IE9 Compat Modes */
    src: url('%s?#iefix') format('embedded-opentype'),
         url('%s') format('woff'),
         url('%s')  format('truetype');
}

""" % (font_family,
        font_style,
        font_weight,
        basename(eot_file_name),
        basename(eot_file_name),
        basename(woff_file_name),
        basename(ttf_file_name) )
                else:
                    self.css += """@font-face {
    font-family: '%s';
    font-style: '%s';
    font-weight: '%s';
    src: url('%s') format('woff'),
         url('%s')  format('truetype');
}

""" % (font_family,
        font_style,
        font_weight,
        basename(woff_file_name),
        basename(ttf_file_name) )
        
        if self.css:
            c = codecs.open(join(dirname(self.infiles[0]), 'webfonts', 'style.css'),'w','UTF-8')
            c.write(self.css)
            c.close()

    def afdko(self):
        import ufo2fdk
        from robofab.objects.objectsRF import RFont
        compiler = ufo2fdk.OTFCompiler()
        for infile in self.infiles:
            outfile = splitext(infile)[0] + '.otf'
            font = RFont(infile)
            compiler.compile(font, outfile, releaseMode=True)

