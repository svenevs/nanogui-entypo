# Entypo+ Font Generator

Generate the font files for [Entypo+][entypo] using the excellent [fontcustom][fc]
tool.  This repository only exists to support embedding the fonts in
[NanoGUI][nanogui].

I make zero claims to ownership of these materials.  See the
[Attribution](#attribution) section for who owns the copyright to what.

## Generate Yourself

1. Follow the [installation instructions][install] for `fontcustom`.
2. Execute `rake` in this directory.

You may want to change the desired `output` in `config/fontcustom.yml` for however
you may want to use this.  I needed this to go into a Sphinx `_static` directory.
You may also want to change the `css_selector` to just be `.icon-{{glyph}}`.  I
prefixed with `entypo` to prevent clashes with the Sphinx theme icons.

There's probably a way to do this directly, but I couldn't figure out how to
change things using `fontcustom` without just flattening the output directory
structure to contain the fonts and css.

## NanoGUI Generation

The reason this repo exists is to update the [NanoGUI][nanogui] fonts.  Be warned
that this likely has zero application to you.  We needed all resources embedded in
a single `.ttf` file to make it accessible for embedding in the library itself.

If you can figure out what this all is doing, more power to you -- feel free to
use it yourself provided that you cite it properly.

## Attribution

I wanted the updated glyphs for Entypo+, all artwork tracked under `icons/Entypo+`
came from downloading Daniel Bruce's hard work at [Entypo+][entypo].  The only
difference in structure of the download is that I moved all of the icons into
the same directory so that they all get globbed together into one `.ttf` file.

This was being done to get the NanoGUI icons updated.  As such, the licensing of
these files is as follows:

1. Directly cite Daniel Bruce for his excellent work with [Entypo+][entypo],
   which has a [Attribution-ShareAlike 4.0][ccsa4] license.

2. I authored this code to directly update [NanoGUI][nanogui].  It is useless
   without the `bin2c` counterparts, and the rest of the framework.  So the
   copyright for the python generation code is property of Wenzel Jakob,
   by way of the [NanoGUI BSD License][nanogui_license].


[entypo]:          http://entypo.com/
[fc]:              https://github.com/FontCustom/fontcustom
[nanogui]:         https://github.com/wjakob/nanogui
[install]:         https://github.com/FontCustom/fontcustom#installation
[ccas4]:           https://creativecommons.org/licenses/by-sa/4.0/
[nanogui_license]: https://github.com/wjakob/nanogui/blob/master/LICENSE.txt
