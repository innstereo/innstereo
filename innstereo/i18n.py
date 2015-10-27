#!/usr/bin/python3

#==============================================================================#
#                                   InnStereo                                  #
#                                                                              #
#    Copyright (c)  2012-2015 Matteo Pasotti <matteo.pasotti@gmail.com>        #
#                                                                              #
#                                                                              #
#    This file was originally part of OpenStereoNet (fork of OpenStereo).      #
#    This file is part of InnStereo since July 2015                            #
#    InnStereo is free software: you can redistribute it and/or modify         #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 2 of the License, or         #
#    (at your option) any later version.                                       #
#                                                                              #
#    InnStereo is distributed in the hope that it will be useful,              #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with InnStereo.  If not, see <http://www.gnu.org/licenses/>.        #
#==============================================================================#

import os, sys
import locale
import gettext
from os.path import join, abspath
from gi.repository import Gtk

class i18n:
    app_name = ""
    language = None

    def __init__(self):
        # The translation files will be under
        # @locale_dir@/@LANGUAGE@/LC_MESSAGES/@app_name@.mo
        self.app_name = "innstereo"
        app_dir = abspath(os.path.dirname(__file__))
        print("app dir:", app_dir)

        # Locale are stored in innstereo/locale
        # .mo files will then be located in innstereo/locale/LANGUAGECODE/LC_MESSAGES/
        locale_dir = abspath(join(app_dir, "locale"))
        print("locale dir", locale_dir)

        if sys.platform == "win32":
            # Set $LANG on MS Windows for gettext
            if os.getenv('LANG') is None:
                lang, enc = locale.getdefaultlocale() #lang is POSIX e.g. de_DE
                print(lang, enc)
                os.environ['LANG'] = lang
                languages = [lang]

            # Set LOCALE_DIR for MS Windows
            import ctypes
            LIB_INTL = abspath(join(app_dir, "../gnome/libintl-8.dll"))
            print("LIB_INTL", LIB_INTL)
            libintl = ctypes.cdll.LoadLibrary(LIB_INTL)
            lc = locale.setlocale(locale.LC_ALL, "")
            locale_dir_g = abspath(join(app_dir, "locale"))
            print(lc) # Returns local. On W e.g. German_Germany.1252
            libintl.bindtextdomain(self.app_name, locale_dir_g)
            libintl.bind_textdomain_codeset(self.app_name, "UTF-8")
        else:
            kwargs = {}
            if sys.version < '3':
                kwargs['unicode'] = 1
            gettext.install(True, localedir=None, **kwargs)

            gettext.find(self.app_name, locale_dir)
            locale.bindtextdomain(self.app_name, locale_dir)

        # Now we need to choose the language. We will provide a list, and gettext
        # will use the first translation available in the list
        default_languages = os.environ.get('LANG', '').split(':')
        default_languages += ['en_US']

        lc, encoding = locale.getdefaultlocale()
        if lc:
            languages = [lc]

        # Concat all languages (env + default locale),
        # and here we have the languages and location of the translations
        languages += default_languages

        gettext.bindtextdomain (self.app_name, locale_dir)
        gettext.textdomain (self.app_name)

        self._language = gettext.translation(self.app_name, locale_dir,
                                             languages=languages, fallback=True)

    def language(self):
        return self._language

    def get_ts_domain(self):
        return self.app_name


_ = i18n().language().gettext
  
def translate_gui(builder):
    for obj in builder.get_objects():
        print(obj)
        if (not isinstance(obj, Gtk.SeparatorMenuItem)) and hasattr(obj, "get_label"):
            label = obj.get_label()
            if label is not None:
                obj.set_label(_(label))
        elif hasattr(obj, "get_title"):
            title = obj.get_title()
            if title is not None:
                obj.set_title(_(title))
        if hasattr(obj, "get_tooltip_text"):
            text = obj.get_tooltip_text()
            if text is not None:
                obj.set_tooltip_text(_(text))
