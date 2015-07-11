#==============================================================================#
#        OpenStereo - Open-source, Multiplatform Stereonet Analysis            #
#                                                                              #
#    Copyright (c)  2012-2015 Matteo Pasotti <matteo.pasotti@gmail.com>        #
#                                                                              #
#                                                                              #
#    This file is part of OpenStereo.                                          #
#    OpenStereo is free software: you can redistribute it and/or modify        #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 3 of the License, or         #
#    (at your option) any later version.                                       #
#                                                                              #
#    OpenStereo is distributed in the hope that it will be useful,             #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with OpenStereo.  If not, see <http://www.gnu.org/licenses/>.       #
#==============================================================================#
# -*- coding: utf-8 -*-

import os, sys
import locale
import gettext

class i18n:

	def __init__(self):
		#  The translation files will be under
		#  @locale_dir@/@LANGUAGE@/LC_MESSAGES/@app_name@.mo
		app_name = "innstereo"

		app_dir = os.getcwd()
		locale_dir = os.path.join(app_dir, 'po') 
		# .mo files will then be located in APP_Dir/i18n/LANGUAGECODE/LC_MESSAGES/

		# Now we need to choose the language. We will provide a list, and gettext
		# will use the first translation available in the list
		#
		default_languages = os.environ.get('LANG', '').split(':')
		default_languages += ['en_US']
		default_languages += ['de_DE']
		default_languages += ['it_IT']


		lc, encoding = locale.getdefaultlocale()
		if lc:
			languages = [lc]

		# Concat all languages (env + default locale),
		#  and here we have the languages and location of the translations
		languages += default_languages
		mo_location = locale_dir
	
		kwargs = {}
		if sys.version < '3':
			kwargs['unicode'] = 1
		gettext.install(True,localedir=None,**kwargs)
	
		gettext.find(app_name, mo_location)

	
		gettext.textdomain (app_name)
	
		gettext.bind_textdomain_codeset(app_name, "UTF-8")

		self._language = gettext.translation(app_name, mo_location, languages = languages, fallback = True)

	def language(self):
		return self._language
