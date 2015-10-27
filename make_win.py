import os, sys
from subprocess import call
import nsist

gsettings = "data/org.gtk.innstereo.gschema.xml"

if os.path.isfile(gsettings):
    call("cp data/org.gtk.innstereo.gschema.xml pynsist_pkgs/gnome/share/glib-2.0/schemas/", shell=True)
else:
    print("Copying failed")
    sys.exit()

try:
    call("glib-compile-schemas pynsist_pkgs/gnome/share/glib-2.0/schemas/", shell=True)
except:
    print("GSettings could not be compiled")
    sys.exit()

translations = "po/"

if os.path.isdir("innstereo/locale") is False:
    call("mkdir innstereo/locale", shell=True)

for root, dirs, filenames in os.walk(translations):
    for f in filenames:
        print(f)
        if f[-3:] == ".po":
            command = "msgfmt -o po/{0}.mo po/{0}.po".format(f[:-3])
            call(command, shell=True)

            command = "cp po/{0}.mo pynsist_pkgs/gnome/share/locale/{0}/LC_MESSAGES/innstereo.mo".format(f[:-3])
            call(command, shell=True)

            command = "innstereo/locale/{0}".format(f[:-3])
            if os.path.isdir(command) == False:
                call("mkdir {}".format(command), shell=True)

            command = "innstereo/locale/{0}/LC_MESSAGES/".format(f[:-3])
            if os.path.isdir(command) == False:
                call("mkdir {}".format(command), shell=True)

            command = "cp po/{0}.mo innstereo/locale/{0}/LC_MESSAGES/innstereo.mo".format(f[:-3])
            call(command, shell=True)

            command = "rm po/{}.mo".format(f[:-3])
            call(command, shell=True)


call("python3 -m nsist installer.cfg", shell=True)

sys.exit()
#The code below is currently not used
appname = "InnStereo"
version = "beta3"
shortcuts = [{"entry_point": "innstereo:startup",
             "extra_preamble": "gnome_preamble.py",
             "console": "false"}]
icon = "innstereo_icon.ico"
icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), icon))
pkg_list = ["innstereo", "gi", "cairo", "dbus", "gnome", "pygtkcompat",
            "numpy", "matplotlib", "six", "dateutil", "pyparsing", "scipy",
            "mplstereonet"]
inst_name = "InnStereo {}".format(version + " {}")

installer64 = nsist.InstallerBuilder(appname, version, shortcuts,
                                     icon=icon_path,
                                     packages=pkg_list,
                                     extra_files=None,
                                     py_version="3.4.3",
                                     py_bitness=64,
                                     py_format="installer",
                                     build_dir="build/nsis",
                                     installer_name=inst_name.format("64bit"),
                                     nsi_template=None,
                                     exclude=None)

installer64.run()

