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

### Minor Divergence from Entypo+

Because these are getting used to embed in a C++ program with some `#define`
directives, three icons were changed since `+` and `%` cannot be used (and the
resultant output was some awkward `__` or trailing `_`):

1. `google+.svg` -> `google-plus.svg`
2. `google+-circled.svg` -> `google-plus-circled.svg`
3. `resize-100%.svg` -> `resize-100-percent.svg`

More concretely, though, the `diff` is relevant here as I manually edited the
`.svg` images attributes using `vim`.  Since I'm doing this on a Unix system,
it seems the line ending also got changed.  This did not cause issues for me
but it may be a problem?  I manually added the `^M` back in the diff, though
it likely won't display online.  Basically, just `revert` that commit if it
is giving you trouble, but I really don't expect it to.

```diff
diff --git a/icons/Entypo+/google+-with-circle.svg b/icons/Entypo+/google-plus-with-circle.svg
similarity index 95%
rename from icons/Entypo+/google+-with-circle.svg
rename to icons/Entypo+/google-plus-with-circle.svg
index f268cd9..193861b 100644
--- a/icons/Entypo+/google+-with-circle.svg
+++ b/icons/Entypo+/google-plus-with-circle.svg
@@ -1,7 +1,7 @@
 <?xml version="1.0" encoding="utf-8"?>
 <!-- Generator: Adobe Illustrator 18.1.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
 <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
-<svg version="1.1" id="Google_x2B__w_x2F__circle" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
+<svg version="1.1" id="Google_plus_w_x2F__circle" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     x="0px" y="0px" viewBox="0 0 20 20" enable-background="new 0 0 20 20" xml:space="preserve">
 <path d="M10,0.4c-5.302,0-9.6,4.298-9.6,9.6s4.298,9.6,9.6,9.6s9.6-4.298,9.6-9.6S15.302,0.4,10,0.4z M9.447,14.121
    c-0.603,0.293-1.252,0.324-1.503,0.324c-0.048,0-0.075,0-0.075,0s-0.023,0-0.054,0c-0.392,0-2.343-0.09-2.343-1.867
diff --git a/icons/Entypo+/google+.svg b/icons/Entypo+/google-plus.svg
similarity index 95%
rename from icons/Entypo+/google+.svg
rename to icons/Entypo+/google-plus.svg
index f364754..823c3a8 100644
--- a/icons/Entypo+/google+.svg
+++ b/icons/Entypo+/google-plus.svg
@@ -1,7 +1,7 @@
 <?xml version="1.0" encoding="utf-8"?>
 <!-- Generator: Adobe Illustrator 18.1.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
 <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
-<svg version="1.1" id="Google_x2B_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px"
+<svg version="1.1" id="Google_plus" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px"
     y="0px" viewBox="0 0 20 20" enable-background="new 0 0 20 20" xml:space="preserve">
 <path d="M1.989,5.589c0,1.494,0.499,2.572,1.482,3.205c0.806,0.52,1.74,0.598,2.226,0.598c0.118,0,0.213-0.006,0.279-0.01
    c0,0-0.154,1.004,0.59,1.996H6.532c-1.289,0-5.493,0.269-5.493,3.727c0,3.516,3.861,3.695,4.636,3.695
diff --git a/icons/Entypo+/resize-100%.svg b/icons/Entypo+/resize-100-percent.svg
similarity index 75%
rename from icons/Entypo+/resize-100%.svg
rename to icons/Entypo+/resize-100-percent.svg
index 1493bea..15fd572 100644
--- a/icons/Entypo+/resize-100%.svg
+++ b/icons/Entypo+/resize-100-percent.svg
@@ -1,7 +1,7 @@
 <?xml version="1.0" encoding="utf-8"?>
 <!-- Generator: Adobe Illustrator 18.1.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
 <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
-<svg version="1.1" id="Resize_100_x25_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px"
+<svg version="1.1" id="Resize_100_percent" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px"
     y="0px" viewBox="0 0 20 20" enable-background="new 0 0 20 20" xml:space="preserve">
 <path d="M4.1,14.1L1,17l2,2l2.9-3.1L8,18v-6H2L4.1,14.1z M19,3l-2-2l-2.9,3.1L12,2v6h6l-2.1-2.1L19,3z"/>
 </svg>
```

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
[ccsa4]:           https://creativecommons.org/licenses/by-sa/4.0/
[nanogui_license]: https://github.com/wjakob/nanogui/blob/master/LICENSE.txt
