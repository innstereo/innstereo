import os, sys
from os.path import join
from subprocess import call

version = "beta6"
localizations = ["de", "el", "es", "fr", "he", "hu", "it", "mn", "nl", "pt-PT",
                 "sk", "sr-Cyrl", "sr-Latn", "sv", "tr", "uz"]
gtk_locals = {"pt_PT": "pt",
              "sr_Cyrl": "sr",
              "sr_Latn": "sr@latin",
              "uz": "uz@cyrillic"}
translations = "po/"

for lc in localizations:
    print("Downloading Translation from Zanata:", lc)
    cmd = "zanata po pull --project-id=innstereo --project-version={} --lang={} --dstdir=po".format(version, lc)
    call(cmd, shell=True)

for root, dirs, filenames in os.walk(translations):
    for f in filenames:
        if f[-3:] == ".po" and f[:-3] in gtk_locals:
            current = f[:-3]
            new = gtk_locals[current]
            print("Rename:", current, "-->", new)
            cmd = "mv po/{}.po po/{}.po".format(current, new)
            call(cmd, shell=True)

for root, dirs, filenames in os.walk(translations):
    for f in filenames:
        if f[-3:] == ".po":
            # Use try except in case there is an error in RTL translation
            command = "msgfmt -o po/{0}.mo po/{0}.po".format(f[:-3])
            call(command, shell=True)

            command = "innstereo/locale/"
            if os.path.isdir(command) == False:
                call("mkdir {}".format(command), shell=True)

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

