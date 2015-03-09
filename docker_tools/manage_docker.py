#!/usr/bin/env python
# coding: utf-8
"""
A script to manage and package Docker files.
"""

import argparse
import logging
import subprocess

log = logging.getLogger(__name__)


def main(args):
  if args.subcommand == 'export':
    subprocess.check_call('git rev-parse --verify {hash}^{{commit}}'
                          .format(hash=args.hash), shell=True)
    subprocess.check_call('mkdir -p {export_path}'
                          .format(export_path=args.export_path),
                          shell=True)
    subprocess.check_call('(cd {repository_path} && git archive {hash} | '
                          'tar -x -C {export_path})'.format(
                            repository_path=args.repository_path,
                            hash=args.hash,
                            export_path=args.export_path),
                          shell=True)
  elif args.subcommand == 'build':
    subprocess.check_call('(docker build {no_cache} -t {tag} '
                          '{dockerfile_directory})'.format(
                            no_cache=('--no-cache=true' if args.no_cache
                                      else ''),
                            tag=args.tag,
                            dockerfile_directory=args.dockerfile_directory),
                          shell=True)
  elif args.subcommand == 'push':
    subprocess.check_call('(docker push {tag})'.format(tag=args.tag),
                          shell=True)


def process_args():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help='What subcommand to run',
                                     dest='subcommand')

  export_parser = subparsers.add_parser(
      'export',
      help='Export a repository hash to a given location.')
  export_parser.add_argument('--hash', required=True,
                             help='A git hash to export')
  export_parser.add_argument('--repository-path', required=True,
                             help='A path to the git repository')
  export_parser.add_argument('--export-path', required=True,
                             help='A path to export to')

  build_parser = subparsers.add_parser(
      'build',
      help='Build a dockerfile at a given location')
  build_parser.add_argument('--dockerfile-directory', required=True,
                            help='The directory containing a Dockerfile')
  build_parser.add_argument('--tag', required=True,
                            help=('The tag for the built image (e.g., '
                                  'chronology/jia:v0.7.2'))
  build_parser.add_argument('--no-cache', action='store_true',
                            help='Allow docker caching?')

  push_parser = subparsers.add_parser(
      'push',
      help='Push a built and tagged image')
  push_parser.add_argument('--tag', required=True,
                           help=('The tag for the built image (e.g., '
                                 'chronology/jia:v0.7.2)'))

  args = parser.parse_args()
  return args


if __name__ == '__main__':
  main(process_args())
