#!/usr/bin/env python
#
# Copyright 2015 Joshua Malone
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for YWorksURLProvider"""

import os
import urllib2
import xml.etree.ElementTree as ET

from autopkglib import Processor, ProcessorError

__all__ = ["ETeksURLProvider"]

check_url = "http://www.sweethome3d.com/SweetHome3DUpdates.xml"
base_prod_url = "http://downloads.sourceforge.net/project/sweethome3d/SweetHome3D"

prods = { "Installer" : "Installer DMG" }


class ETeksURLProvider(Processor):
    """This processor obtains a download URL for the latest version of Sweet Home 3D"""
    description = __doc__
    input_variables = {
        "product_name": {
	    "required": True,
	    "description": "Which product to fetch: Installer, etc...",
	},
    }
    output_variables = {
        "url": {
	    "description": "URL to latest version of the product.",
	},
    }

    def main(self):
        """Provide a download URL for Sweet Home 3D"""
	valid_prods = prods.keys()
	product_name = self.env["product_name"]
	if product_name not in valid_prods:
	    raise ProcessorError("product_name %s is invalid" % (product_name) )

	# Get the xml file of updates
	try:
	    fref = urllib2.urlopen(check_url)
	    xmldata = fref.read()
	    fref.close()
	except BaseException as err:
	    raise ProcessorError("Can't download %s: %s" % (check_url, err))

	# Create download link
	tree = ET.fromstring(xmldata)
	for installer in tree.findall("./update/[@id='SweetHome3D#%s']" % product_name):
	    if (installer.attrib['operatingSystem'] == 'Mac OS X'):
		version=installer.attrib['version']

	download_url="%s/SweetHome3D-%s/SweetHome3D-%s-macosx.dmg" % (base_prod_url, version, version)
	self.env["url"] = download_url
	self.output("Found URL as %s" % self.env["url"])

if __name__ == "__main__":
    PROCESSOR = ETeksURLProvider()
    PROCESSOR.execute_shell()
