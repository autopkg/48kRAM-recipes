#!/usr/bin/python

"""See docstring for OSXfuseURLProvider class"""

from __future__ import absolute_import
import os
import urllib2
import plistlib

from autopkglib import Processor, ProcessorError

__all__ = ["OSXFuseURLProvider"]

check_url = "http://osxfuse.github.com/releases/DeveloperRelease.plist"

class OSXFuseURLProvider(Processor):
    """Provides a URL to download the latest version of OSXFUSE"""
    description = __doc__

    input_variables = {
        "os_version" : {
	    "description" : "OSX version to be compatible with",
	    "required" : True,
	}
    }
    output_variables = {
        "url": {
	    "description" : "Download URL",
	},
    }

    def main(self):
	'''Find the download URL'''
	os_version = self.env["os_version"]
	try:
	    plist_str = urllib2.urlopen(check_url).read()
	except BaseException as err:
	    raise ProcessorError("Unable to get updates list: '%s'" % err)
	
	try:
	    plist = plistlib.readPlistFromString(plist_str)
	except BaseException as err:
	    raise ProcessorError("Update check returned unexpected data: '%s'" % err)
	
	rules = plist.get('Rules')
	for rule in rules:
	    if 'beginswith "%s" ' % os_version in rule.Predicate:
	        url = rule.Codebase
		self.env["url"] = url
		self.output("Found URL %s" % self.env["url"] )

if __name__ == "__main__":
    PROCESSOR = OSXFuseURLProvider()
    PROCESSOR.execute_shell()
