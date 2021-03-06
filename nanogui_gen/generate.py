#!/usr/bin/env python3

import os
import codecs
from io import BytesIO
import re
import textwrap


# Entypo+ has 411 icons at the time of writing this
EXPECTED_NUM_ICONS = 411


if __name__ == "__main__":
    # Make sure we're in the same directory to avoid overwriting things
    # in parent directory (specifically entypo.ttf)
    file_loc = os.path.dirname(os.path.abspath(__file__))
    curr_dir = os.path.abspath(os.getcwd())

    if file_loc != curr_dir:
        raise RuntimeError(
            "Please execute this script in directory [{0}]".format(file_loc)
        )

    # Make sure the CSS file exists / has been generated
    css_file = os.path.abspath(
        os.path.join(file_loc, "..", "_static", "entypo.css")
    )
    if not os.path.exists(css_file):
        raise RuntimeError(
            "[{0}] does not exist.  Make sure you already generated it.".format(
                css_file
            )
        )

    # Generate entypo.h
    cdefs = []
    num_matches = 0
    longest = 0
    # .entypo-icon-location:before { content: "\e724"; }
    icon_re = re.compile(r'\.entypo-icon-(.+):before { content: "\\(.+)"; }')
    with codecs.open(css_file, "r", "utf-8") as css:
        for line in css:
            match = icon_re.match(line)
            if match:
                num_matches += 1
                icon_name, icon_code = match.groups()
                icon_def = "#define ENTYPO_ICON_{0}".format(
                    icon_name.replace("-", "_").upper()
                )
                # {code:0>8} format spec says using code variable, align it to
                # the right and make it a fixed width of 8 characters, padding
                # with a 0.  AKA zero-fill on the left until 8 char long
                icon_code = "0x{code:0>8}".format(code=icon_code.upper())
                cdefs.append((icon_name, icon_def, icon_code))
                longest = max(longest, len(icon_def))


    if num_matches == EXPECTED_NUM_ICONS:
        print("Found exactly [{0}] icons, as expected.".format(num_matches))
    else:
        raise RuntimeError(
            "Found [{0}] icons, expected [{1}]".format(num_matches,
                                                       EXPECTED_NUM_ICONS)
        )

    entypo_h = open("entypo.h", "w")
    entypo_h.write(textwrap.dedent(r'''
        /*
             NanoGUI was developed by Wenzel Jakob <wenzel.jakob@epfl.ch>.
             The widget drawing code is based on the NanoVG demo application
             by Mikko Mononen.

             All rights reserved. Use of this source code is governed by a
             BSD-style license that can be found in the LICENSE.txt file.
         */

        /* Developer note: need to make a change to this file?
         * Please raise an Issue on GitHub describing what needs to change.  This file
         * was generated, so the scripts that generated it need to update as well.
         */

        /**
         * \file nanogui/entypo.h
         *
         * \brief This is a list of icon codes for the ``entypo.ttf`` font by Daniel Bruce.
         *
         * \rst
         *
         * This file defines the full listing of `Entypo <http://www.entypo.com/>`_
         * icons available in NanoGUI.  Please note that if viewing the documentation
         * on the web, your browser may display the icons differently than what they
         * look like in NanoGUI.  Run the one of the :ref:`nanogui_example_icons`
         * executables to see what they all look like in NanoGUI.
         *
         * .. note::
         *
         *    Constants you may have used in the past may no longer exist, e.g.
         *    the name may have changed slightly.  For example, ``ENTYPO_ICON_CIRCLED_HELP``
         *    is renamed to ``ENTYPO_ICON_HELP_WITH_CIRCLE``.
         *
         * .. warning::
         *
         *    Some icons have a "small" variant, e.g. ``ENTYPO_ICON_CHEVRON_SMALL_LEFT``
         *    is smaller than ``ENTYPO_ICON_CHEVRON_LEFT``.  While these "small" icons
         *    can be used, they may not be positioned correctly.  If you experience this
         *    you can, instead of using the "small" variant, use the "regular" icon and
         *    call the :func:`nanogui::Widget::setIconExtraScale` function with a value
         *    of **less than** ``1.0`` to scale the icon size down.
         *
         * .. tip::
         *
         *    In C++, ``#include <nanogui/entypo.h>`` to gain access to the ``#define``
         *    shown in these docs.  In Python, ``from nanogui import entypo``.  So in the
         *    below table, when you see ``ENTYPO_ICON_FLOW_TREE`` that is for C++, and
         *    when you see ``ICON_FLOW_TREE``, that is for Python, and you would access
         *    it using ``entypo.ICON_FLOW_TREE``.
         *
         * The following icons are available:
         *
         * .. raw:: html
         *
         *    <center>
         *      <div class="wy-table-responsive">
         *        <table class="docutils" border=1>
         *          <colgroup>
         *            <col width="55%" align="center"/>
         *            <col width="10%" align="center" />
         *            <col width="35%" align="center"/>
         *          </colgroup>
         *          <thead valign="bottom">
         *            <tr class="row-odd">
         *              <th class="head" align="center">C++ Definition</th>
         *              <th class="head" align="center">Icon</th>
         *              <th class="head" align="center">Python Definition</th>
         *            </tr>
         *          </thead>
         *          <tbody valign="top">
    '''.replace("\n", "", 1)))  # remove empty line at top

    constants_entypo = open("constants_entypo.cpp", "w")
    constants_entypo.write(textwrap.dedent('''
        #ifdef NANOGUI_PYTHON

        #include "python.h"

        /* Developer note: need to make a change to this file?
         * Please raise an Issue on GitHub describing what needs to change.  This file
         * was generated, so the scripts that generated it need to update as well.
         */

        void register_constants_entypo(py::module &m) {
            /* Entypo constants */
            {
                #define C(name) g.attr("ICON_" #name) = py::int_(ENTYPO_ICON_##name);
                py::module g = m.def_submodule("entypo");
    '''))

    # First write the docstring for entypo_h so the API isn't littered with `define ENTYPO_ICON X`
    # all over the place, which significantly increases build time (file generated for every def).
    flip = True  # thead was odd, start on even
    for icon_name, icon_def, icon_code in cdefs:
        if flip:
            row_kind = "row-even"
        else:
            row_kind = "row-odd"
        flip = not flip

        # icon_def is `#define ENTYPO_ICON_X`
        cpp_def = icon_def.split(" ")[1]
        py_def  = cpp_def.split("ENTYPO_ICON_")[1]
        pybind  = "C({0});".format(py_def)
        py_name = "ICON_{0}".format(py_def)

        entypo_h.write(textwrap.dedent('''
            *            <tr class="{row_kind}">
            *              <td align="right"><code>{cpp_def}</code></td>
            *              <td align="center"><span class="entypo-icon-{name}"></span></td>
            *              <td align="left"><code>{py_name}</code>
            *            </tr>
        '''.format(
            row_kind=row_kind,
            cpp_def=cpp_def,
            name=icon_name,
            py_name=py_name
        )).replace("\n*", "\n *").replace("\n", "", 1).rstrip())
        entypo_h.write("\n")  # rstrip removed two, we need 1

        constants_entypo.write("        {pybind}\n".format(pybind=pybind))

    # Now close the docstring and actually write the definitions
    entypo_h.write(textwrap.dedent(r'''
         *          </tbody>
         *        </table>
         *      </div><!-- wy-table-responsive -->
         *    </center>
         *
         * \endrst
         */

        #pragma once

        // prevent individual pages from being generated for all of these
        #if !defined(DOXYGEN_SHOULD_SKIP_THIS)

    '''.replace("\n", "", 1)))  # replace leading \n (NECESSARY!)

    # close the pybind
    constants_entypo.write(textwrap.dedent('''
                #undef C
            }
        }

        #endif
    '''))

    for icon_name, icon_def, icon_code in cdefs:
        entypo_h.write("{definition:<{longest}} {code}\n".format(
            definition=icon_def,
            longest=longest,
            code=icon_code
        ))

    entypo_h.write("\n#endif // DOXYGEN_SHOULD_SKIP_THIS\n")

    entypo_h.close()
    constants_entypo.close()

    # generate the example icon programs
    cpp_example = open("example_icons.cpp", "w")

    # write the header of the cpp example
    cpp_example.write(textwrap.dedent(r'''
        /*
            src/example_icons.cpp -- C++ version of an example application that shows
            all available Entypo icons as they would appear in NanoGUI itself.  For a Python
            implementation, see '../python/example_icons.py'.

            NanoGUI was developed by Wenzel Jakob <wenzel.jakob@epfl.ch>.
            The widget drawing code is based on the NanoVG demo application
            by Mikko Mononen.

            All rights reserved. Use of this source code is governed by a
            BSD-style license that can be found in the LICENSE.txt file.
        */

        /* Developer note: need to make a change to this file?
         * Please raise an Issue on GitHub describing what needs to change.  This file
         * was generated, so the scripts that generated it need to update as well.
         */

        #include <nanogui/nanogui.h>
        using namespace nanogui;

        class EscapeScreen : public nanogui::Screen {
        public:
            EscapeScreen(const Vector2i &size, const std::string &title, bool resizable)
                : nanogui::Screen(size, title, resizable) { }

            virtual ~EscapeScreen() { /* nothing to free */ }

            // allow <ESCAPE> to exit
            virtual bool keyboardEvent(int key, int scancode, int action, int modifiers) override {
                if (key == GLFW_KEY_ESCAPE && modifiers == 0) {
                    setVisible(false);
                    return true;
                }

                return Screen::keyboardEvent(key, scancode, action, modifiers);
            }
        };

        // Convenience macro for creating an IconBox. Make sure you put a semicolon after the call to this macro!
        #define ADD_ICON(parent, icon, boxWidth) \
            new IconBox(parent, #icon, icon, boxWidth)

        class IconBox : public Widget {
        public:
            IconBox(Widget *parent, const std::string &name, int icon, int width)
                : Widget(parent) {

                this->setLayout(new BoxLayout(Orientation::Horizontal));

                auto *b = new Button(this, "", icon);
                b->setFixedWidth(40);

                auto *text = new TextBox(this, name);
                text->setDefaultValue(name);
                text->setEditable(true);
                /* Return false essentially makes it not possible to actually edit this text
                 * box, but keeping it editable=true allows selection for copy-paste.  If the
                 * text box is not editable, then the user cannot highlight it.
                 */
                text->setCallback([](const std::string &) { return false; });
                text->setFont("mono-bold");
                text->setFixedWidth(width - 40);
            }
        };

        int main(int /* argc */, char ** /* argv */) {
            nanogui::init();

            /* scoped variables */ {
                static constexpr int width      = 1000;
                static constexpr int half_width = width / 2;
                static constexpr int height     = 800;

                // create a fixed size screen with one window
                EscapeScreen *screen = new EscapeScreen({width, height}, "NanoGUI Icons", false);
                Window *window = new Window(screen, "");
                window->setPosition({0, 0});
                window->setFixedSize({width, height});

                // attach a vertical scroll panel
                auto vscroll = new VScrollPanel(window);
                vscroll->setFixedSize({width, height});

                // vscroll should only have *ONE* child. this is what `wrapper` is for
                auto wrapper = new Widget(vscroll);
                wrapper->setFixedSize({width, height});
                wrapper->setLayout(new GridLayout());// defaults: 2 columns

                ////////////////////////////////////////////////////////////////////////
                ////////////////////////////////////////////////////////////////////////
                ////////////////////////////////////////////////////////////////////////
    ''').lstrip())

    for icon_name, icon_def, icon_code in cdefs:
        # icon_def is `#define ENTYPO_ICON_X`
        cpp_def = icon_def.split(" ")[1]
        cpp_example.write("        ADD_ICON(wrapper, {cpp_def}, half_width);\n".format(cpp_def=cpp_def))

    # close out the cpp example
    cpp_example.write(textwrap.dedent('''
                ////////////////////////////////////////////////////////////////////////
                ////////////////////////////////////////////////////////////////////////
                ////////////////////////////////////////////////////////////////////////

                screen->performLayout();
                screen->setVisible(true);

                nanogui::mainloop();
            }

            nanogui::shutdown();
            return 0;
        }
    ''').replace("\n", "", 1))
    cpp_example.close()

    # <3 python
    with open("example_icons.py", "w") as py_example:
        py_example.write(textwrap.dedent('''
            # python/example_icons.py -- Python version of an example application that shows
            # all available Entypo icons as they would appear in NanoGUI itself.  For a C++
            # implementation, see '../src/example_icons.cpp'.
            #
            # NanoGUI was developed by Wenzel Jakob <wenzel.jakob@epfl.ch>.
            # The widget drawing code is based on the NanoVG demo application
            # by Mikko Mononen.
            #
            # All rights reserved. Use of this source code is governed by a
            # BSD-style license that can be found in the LICENSE.txt file.

            # Developer note: need to make a change to this file?
            # Please raise an Issue on GitHub describing what needs to change.  This file
            # was generated, so the scripts that generated it need to update as well.

            import gc

            import nanogui
            from nanogui import Screen, Window, Widget, GridLayout, VScrollPanel, Button
            from nanogui import entypo

            class EscapeScreen(nanogui.Screen):
                def __init__(self, size, title, resizable):
                    super(EscapeScreen, self).__init__(size, title, resizable)

                # allow <ESCAPE> to exit
                def keyboardEvent(self, key, scancode, action, modifiers):
                    if key == nanogui.glfw.KEY_ESCAPE and modifiers == 0:
                        self.setVisible(False)
                        return True

                    return super(EscapeScreen, self).keyboardEvent(key, scancode, action, modifiers)


            class IconBox(nanogui.Widget):
                def __init__(self, parent, name, icon, width):
                    super(IconBox, self).__init__(parent)

                    self.setLayout(nanogui.BoxLayout(nanogui.Orientation.Horizontal))

                    b = nanogui.Button(self, "", icon)
                    b.setFixedWidth(40)

                    text = nanogui.TextBox(self, name)
                    text.setDefaultValue(name)
                    text.setEditable(True)
                    # Return false essentially makes it not possible to actually edit this text
                    # box, but keeping it editable=true allows selection for copy-paste.  If the
                    # text box is not editable, then the user cannot highlight it.
                    text.setCallback(lambda x: False)
                    text.setFont("mono-bold")
                    text.setFixedWidth(width - 40)


            if __name__ == "__main__":
                nanogui.init()

                width      = 1000
                half_width = width // 2
                height     = 800

                # create a fixed size screen with one window
                screen = EscapeScreen((width, height), "NanoGUI Icons", False)
                window = Window(screen, "")
                window.setPosition((0, 0))
                window.setFixedSize((width, height))

                # attach a vertical scroll panel
                vscroll = VScrollPanel(window)
                vscroll.setFixedSize((width, height))

                # vscroll should only have *ONE* child. this is what `wrapper` is for
                wrapper = Widget(vscroll)
                wrapper.setFixedSize((width, height))
                wrapper.setLayout(GridLayout())  # defaults: 2 columns

                # NOTE: don't __dict__ crawl in real code!
                # this is just because it's more convenient to do this for enumerating all
                # of the icons -- see cpp example for alternative...
                for key in entypo.__dict__.keys():
                    if key.startswith("ICON_"):
                        IconBox(wrapper, key, entypo.__dict__[key], half_width)

                screen.performLayout()
                screen.drawAll()
                screen.setVisible(True)

                nanogui.mainloop()

                del screen
                gc.collect()

                nanogui.shutdown()
        ''').lstrip())
