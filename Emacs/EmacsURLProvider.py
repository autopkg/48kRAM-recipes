#!/usr/bin/python
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
"""See docstring for EmacsURLProvider"""

from __future__ import absolute_import

import subprocess
import xml.etree.ElementTree as ET

from autopkglib import Processor, ProcessorError

__all__ = ["EmacsURLProvider"]

check_url = "https://emacsformacosx.com/atom/release"


class EmacsURLProvider(Processor):
    """This processor obtains a download URL for the latest version of GNU Emacs for OSX"""
    description = __doc__
    input_variables = {
    }
    output_variables = {
        "url": {
            "description": "URL to latest version of the product.",
        },
    }

    def main(self):
        """Provide a download URL for GNU Emacs for OSX"""
        # Get the xml file of updates
        try:
            xmldata = subprocess.check_output(('/usr/bin/curl',
                                               '--silent',
                                               '--location',
                                               check_url))
        except BaseException as err:
            raise ProcessorError("Can't download %s: %s" % (check_url, err))

        # Grab the first download link of the right type
        root = ET.fromstring(xmldata)
        for link in root.iter('{http://www.w3.org/2005/Atom}link'):
            if link.attrib['type'] == 'binary/octet-stream':
                url = link.attrib['href']
                break

        self.env["url"] = url
        self.output("Found URL as %s" % self.env["url"])

if __name__ == "__main__":
    PROCESSOR = EmacsURLProvider()
    PROCESSOR.execute_shell()
