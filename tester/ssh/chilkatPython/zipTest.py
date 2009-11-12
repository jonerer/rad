import sys
import chilkat

zip = chilkat.CkZip()

#  Any string unlocks the component for the 1st 30-days.
success = zip.UnlockComponent("Anything for 30-day trial")
if (success != True):
    print zip.lastErrorText
    sys.exit()

success = zip.NewZip("zipTest.zip")
if (success != True):
    print zip.lastErrorText()
    sys.exit()

recurse = False
zip.AppendFiles("*.html",recurse)

success = zip.WriteZipAndClose()
if (success != True):
    print zip.lastErrorText()
    sys.exit()

print "Test zip created."
