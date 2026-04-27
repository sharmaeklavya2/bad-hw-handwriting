#!/usr/bin/env python3
import os
import json
from os.path import join as pjoin
import argparse
import jinja2

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', default=pjoin(ROOT_DIR, 'index.html.jinja2'),
        help='Path to Jinja2 template (default: <repo>/index.html.jinja2)')
    parser.add_argument('--entries', default=pjoin(ROOT_DIR, 'entries.json'),
        help='Path to entries in JSON (default: <repo>/entries.json)')
    # parser.add_argument('--img-dir', default=pjoin(ROOT_DIR, 'img'),
        # help='Path to directory containing images (default: <repo>/img)')
    parser.add_argument('-o', '--output', default=pjoin(ROOT_DIR, 'index.html'),
        help='Path to output html file (default: <repo>/index.html)')
    args = parser.parse_args()

    with open(args.entries) as fp:
        entries = json.load(fp)
    with open(args.template) as fp:
        template = jinja2.Template(fp.read())
    output = template.render({'entries': entries})
    with open(args.output, 'w') as fp:
        fp.write(output)


if __name__ == '__main__':
    main()
