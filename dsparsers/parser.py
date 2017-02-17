import uuid
import requests
import os
import math

from tqdm import tqdm

class Parser():
    "Base class for file-based dataset parsers."

    # stores triples (<URL of file>, <local path to store>, <sha1sum digest>) 
    dsurls = None     

    def load_urls(self):
        """Preloads files defined in dsurls.

        All files will be downloaded once in
        accordance to their hash digests."""

        if self.dsurls is None:
            # we have nothing to load
            return

        for (url, out, hbase) in self.dsurls:
            # check if file does exist already
            if os.path.isfile(out):
                # and it's hex digest is fine
                hsum = os.popen(str.format('sha1sum {0}', out)).read().split(' ')[0]
                if hsum == hbase:
                    return

            # create directories for the output file
            os.makedirs(os.path.dirname(out), exist_ok=True)

            # make a GET request and check if it's OK
            resp = requests.get(url, stream=True)
            if resp.status_code is not 200:
                # it's not OK
                return

            print(str.format('Downloading {0}...', url))
            # write response contents to file by chunks
            with open(out, 'wb') as handle:
                chunks = math.ceil(int(resp.headers['content-length']) / 65536)
                for data in tqdm(resp.iter_content(chunk_size=65536), total=chunks):
                    handle.write(data)

    def progress(self, snum):
        # inner wrapper for tqdm progress bar for sample parsing
        return tqdm(range(snum), desc='parsing', unit='sample')
