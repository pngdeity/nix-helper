#!/usr/bin/env python3

from __future__ import annotations
import dataclasses
import pathlib
import click
import subprocess
import json
import rich

from zilch import NixPackage, console
from cli import cli

SEARCH_CMD = lambda source, term: ['nix', 'search', source, *term, '--json']

@cli.command(no_args_is_help=True)  # @cli, not @click!
@click.argument('term', nargs=-1)
@click.option('--source', default="nixpkgs")
def search(term, source):
    o = subprocess.run(
        SEARCH_CMD(source, term),
        capture_output=True,
        check=True
    )
    packages = []
    for k, v in json.loads(o.stdout).items():
        p = NixPackage(source, k, None, v['version'], v['description'])
        console.print(f"[green]{p.name}[/green] ({p.version})")
        if p.description is not '':
            console.print(f"  {p.description}")
        console.print('')