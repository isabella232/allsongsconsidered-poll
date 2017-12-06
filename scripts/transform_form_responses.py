#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import arrow


# GLOBAL SETTINGS
cwd = os.path.dirname(__file__)
INPUT_PATH = os.path.join(cwd, '../output')
OUTPUT_PATH = os.path.join(cwd, '../output')
HEADER = ['id', 'timestamp', 'day', 'album', 'artist', 'ranking']


def run():
    """
    Parse allsongsconsidered form results and normalize it to be deduped.
    """

    # Create output files folder if needed
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    rows = []
    with open('%s/2017_responses_normalized.csv' % (OUTPUT_PATH), 'w') as fo:
        writer = csv.writer(fo)
        writer.writerow(HEADER)
        with open('%s/2017_responses_clean.csv' % (INPUT_PATH)) as fi:
            reader = csv.reader(fi)
            reader.next()
            for idx, row in enumerate(reader):
                # Use a small cache to remove duplicate album-artist entries within a form response
                cache = {}
                if row[0] != '':
                    timestamp = arrow.get(row[0], 'M/D/YYYY H:m:s')
                    for i in range(5):
                        ranking = 5 - i
                        album = row[2*i + 1].strip()
                        artist = row[2*i + 2].strip()
                        key = '-'.join([album, artist])
                        try:
                            cache[key]
                            continue
                        except KeyError:
                            cache[key] = 1

                        if album.strip() != '':
                            rows.append([
                                idx,
                                timestamp,
                                timestamp.day,
                                album.decode('utf-8').encode('ascii', 'ignore'),
                                artist.decode('utf-8').encode('ascii', 'ignore'),
                                ranking
                            ])
            writer.writerows(rows)


if __name__ == '__main__':
    run()
