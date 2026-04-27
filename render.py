#!/usr/bin/env python3

import os
import sys
import json
from os.path import join as pjoin
import argparse
import jinja2
from typing import Any

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def addImgDims(entries: list[dict[str, Any]], imgDir: str) -> None:
    try:
        from PIL import Image
    except ImportError:
        print('Package Pillow is not installed. Not computing width and height of images.', file=sys.stderr)
        return

    for entry in entries:
        fpath = pjoin(imgDir, entry['fname'])
        with Image.open(fpath) as img:
            entry['width'], entry['height'] = img.size


def addMode(entries: list[dict[str, Any]]) -> None:
    for entry in entries:
        if 'mode' not in entry:
            entry['mode'] = 'light'


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', default=pjoin(ROOT_DIR, 'index.html.jinja2'),
        help='Path to Jinja2 template (default: <repo>/index.html.jinja2)')
    parser.add_argument('--entries', default=pjoin(ROOT_DIR, 'entries.json'),
        help='Path to entries in JSON (default: <repo>/entries.json)')
    parser.add_argument('--img-dir', default=pjoin(ROOT_DIR, 'img'),
        help='Path to directory containing images (default: <repo>/img)')
    parser.add_argument('-o', '--output', default=pjoin(ROOT_DIR, 'index.html'),
        help='Path to output html file (default: <repo>/index.html)')
    args = parser.parse_args()

    with open(args.entries) as fp:
        entries = json.load(fp)
    with open(args.template) as fp:
        template = jinja2.Template(fp.read())

    addImgDims(entries, args.img_dir)
    addMode(entries)

    output = template.render({'entries': entries})
    with open(args.output, 'w') as fp:
        fp.write(output)


if __name__ == '__main__':
    main()
