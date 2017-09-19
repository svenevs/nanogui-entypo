#!/usr/bin/env python3

import os
import shutil

if __name__ == "__main__":
    # Make sure we're in the same directory to avoid overwriting things
    # in parent directory (specifically entypo.ttf)
    file_loc = os.path.dirname(os.path.abspath(__file__))
    curr_dir = os.path.abspath(os.getcwd())

    if file_loc != curr_dir:
        raise RuntimeError(
            "Please execute this script in directory [{0}]".format(file_loc)
        )

    # nanogui/
    #     docs/
    #         _static/
    #     include/
    #         nanogui/
    #     python/
    #     src/
    #     resources/
    #         nanogui-entypo/
    #             _static/
    #                 entypo.css
    #                 entypo.eot
    #                 entypo.svg
    #                 entypo.ttf
    #                 entypo.woff
    #                 entypo.woff2
    #             nanogui_gen/  <<< you are here
    nanogui_root    = os.path.abspath("../../..")
    docs_static     = os.path.join(nanogui_root, "docs", "_static")
    include_nanogui = os.path.join(nanogui_root, "include", "nanogui")
    src             = os.path.join(nanogui_root, "src")
    python          = os.path.join(nanogui_root, "python")
    resources       = os.path.join(nanogui_root, "resources")

    gen_root        = os.path.abspath("..")
    gen_static      = os.path.join(gen_root, "_static")

    # make sure they are all here
    entypo_h             = os.path.join(file_loc, "entypo.h")
    constants_entypo_cpp = os.path.join(file_loc, "constants_entypo.cpp")
    cpp_example          = os.path.join(file_loc, "example_icons.cpp")
    py_example           = os.path.join(file_loc, "example_icons.py")

    entypo_css           = os.path.join(gen_static, "entypo.css")
    entypo_eot           = os.path.join(gen_static, "entypo.eot")
    entypo_svg           = os.path.join(gen_static, "entypo.svg")
    entypo_ttf           = os.path.join(gen_static, "entypo.ttf")
    entypo_woff          = os.path.join(gen_static, "entypo.woff")
    entypo_woff2         = os.path.join(gen_static, "entypo.woff2")

    sources = [
        entypo_h,
        constants_entypo_cpp,
        cpp_example,
        py_example,

        entypo_css,
        entypo_eot,
        entypo_svg,
        entypo_ttf,
        entypo_woff,
        entypo_woff2
    ]

    for s in sources:
        if not os.path.exists(s):
            raise RuntimeError(
                "Did you `generate`?  [{0}] does not exist.".format(s)
            )

    # entypo.h -> include/nanogui/entypo.h
    shutil.copy(entypo_h, include_nanogui)
    # constants_entypo.cpp -> python/
    shutil.copy(constants_entypo_cpp, python)
    # entypo.ttf -> resources
    shutil.copy(entypo_ttf, resources)
    # cpp example -> src/
    shutil.copy(cpp_example, src)
    # py example -> python/
    shutil.copy(py_example, python)

    # docs for entypo.h need these all for the html rendering (see the css
    # file at the top, it uses all of them)
    statics = [
        entypo_css,
        entypo_eot,
        entypo_svg,
        entypo_ttf,
        entypo_woff,
        entypo_woff2
    ]
    for s in statics:
        shutil.copy(s, docs_static)

