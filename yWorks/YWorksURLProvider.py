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

from __future__ import absolute_import

from autopkglib import Processor, ProcessorError, URLGetter

__all__ = ["YWorksURLProvider"]


class YWorksURLProvider(URLGetter):
    """This processor obtains a download URL for the latest version of yWorks"""

    description = __doc__
    input_variables = {
        "product_name": {
            "required": True,
            "description": "Product to fetch URL for. Right now, only 'yEd'.",
        },
    }
    output_variables = {
        "url": {"description": "URL to latest version of the given product.",},
    }

    def main(self):
        """Provide a yWorks product download URL"""
        product_name = self.env["product_name"]
        # http://www.yworks.com/products/yed/demo/yEd-CurrentVersion.txt
        base_url = "http://www.yworks.com/products"
        check_url = "%s/%s/demo/%s-CurrentVersion.txt" % (
            base_url,
            product_name.lower(),
            product_name,
        )
        print(check_url)

        # Get the text file
        try:
            txt = self.download(check_url, text=True)
        except BaseException as err:
            raise ProcessorError("Can't download %s: %s" % (check_url, err))

        # Create download link
        latest = txt.rstrip()
        base_prod_url = "http://www.yworks.com/products"
        download_url = "%s/%s/demo/%s-%s_with-JRE10.dmg" % (
            base_prod_url,
            product_name.lower(),
            product_name,
            latest,
        )
        self.env["url"] = download_url
        self.output("Found URL as %s" % self.env["url"])


if __name__ == "__main__":
    PROCESSOR = YWorksURLProvider()
    PROCESSOR.execute_shell()
