#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import mkdir
from os.path import splitext, dirname, sep, join, exists, basename
from subprocess import Popen
from diagnostics import diagnostics, known_compilers, FontError
import codecs

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
                    
                print "name:", name
                print "basename(name):", basename(name)
                woff_file_name = join(outdir, 'webfonts', basename(name) + '.woff')
                ttf_file_name = join(outdir, 'webfonts', basename(name) + '.ttf')
                eot_file_name = join(outdir, 'webfonts', basename(name) + '.eot')

                font.generate(woff_file_name, flags=("round"))
                font.generate(ttf_file_name, flags=("round"))
                if eot:
                    eot_file = open(eot_file_name, 'wb')
                    pipe = Popen(['mkeot', ttf_file_name], stdout=eot_file)
                
                # Generate CSS:
                font_style = "normal"
                if font.italicangle != 0:
                    font_style = "italic"
                font_weight = font.os2_weight
                # http://www.microsoft.com/typography/otspec/os2ver0.htm#wtc
                # ->
                # http://www.w3.org/TR/CSS21/fonts.html#font-boldness
                font_family = font.familyname
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

