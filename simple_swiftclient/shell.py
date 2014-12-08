#!/usr/bin/python -u
# Copyright (c) 2010-2012 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

from optparse import OptionParser, OptionGroup, SUPPRESS_HELP
from os import environ, _exit as os_exit
from sys import argv as sys_argv, exit, stderr

from client import Client

import utils

commands = ('upload')


def immediate_exit(signum, frame):
    stderr.write(" Aborted\n")
    os_exit(2)


def st_upload(options, args):

    values = {
        'username': options.os_username,
        'password': options.os_password,
        'auth_url': options.os_auth_url,
        'tenant_name': options.os_tenant_name,
    }


    container = args[1]
    path = args[2]

    cli = Client(values)

    cli.upload(container, path)

def main(arguments=None):
    if arguments:
        argv = arguments
    else:
        argv = sys_argv

    version = '1.0'
    parser = OptionParser(version='%%prog %s' % version,
                          usage='''
usage: %%prog [--version] [--help]
             [--auth-version <auth_version>]
             [--os-username <auth-user-name>] [--os-password <auth-password>]
             [--os-tenant-name <auth-tenant-name>]
             [--os-auth-url <auth-url>] [--os-auth-token <auth-token>]
             [--os-storage-url <storage-url>] [--os-region-name <region-name>]
             <subcommand> [--help]

Command-line interface to the OpenStack Swift API.

Positional arguments:
  <subcommand>
    upload               Uploads files or directories to the given container.
'''.strip('\n') % globals())
    parser.add_option('--insecure',
                      action="store_true", dest="insecure",
                      default=True,
                      help='Allow swiftclient to access servers without '
                           'having to verify the SSL certificate. '
                           'Defaults to env[SWIFTCLIENT_INSECURE] '
                           '(set to \'true\' to enable).')

    os_grp = OptionGroup(parser, "OpenStack authentication options")
    os_grp.add_option('--os-username',
                      metavar='<auth-user-name>',
                      default=environ.get('OS_USERNAME'),
                      help='OpenStack username. Defaults to env[OS_USERNAME].')
    os_grp.add_option('--os_username',
                      help=SUPPRESS_HELP)
    os_grp.add_option('--os-password',
                      metavar='<auth-password>',
                      default=environ.get('OS_PASSWORD'),
                      help='OpenStack password. Defaults to env[OS_PASSWORD].')
    os_grp.add_option('--os-tenant-name',
                      metavar='<auth-tenant-name>',
                      default=environ.get('OS_TENANT_NAME'),
                      help='OpenStack tenant name. '
                           'Defaults to env[OS_TENANT_NAME].')
    os_grp.add_option('--os_tenant_name',
                      help=SUPPRESS_HELP)
    os_grp.add_option('--os-auth-url',
                      metavar='<auth-url>',
                      default=environ.get('OS_AUTH_URL'),
                      help='OpenStack auth URL. Defaults to env[OS_AUTH_URL].')
    os_grp.add_option('--os_auth_url',
                      help=SUPPRESS_HELP)
    os_grp.add_option('--os-storage-url',
                      metavar='<storage-url>',
                      default=environ.get('OS_STORAGE_URL'),
                      help='OpenStack storage URL. '
                           'Defaults to env[OS_STORAGE_URL]. '
                           'Overrides the storage url returned during auth. '
                           'Will bypass authentication when used with '
                           '--os-auth-token.')
    os_grp.add_option('--os_storage_url',
                      help=SUPPRESS_HELP)

    (options, args) = parser.parse_args(argv[1:])

    if not args or args[0] not in commands:
        parser.print_usage()
        if args:
            exit('no such command: %s' % args[0])
        exit()

    try:
        globals()['st_%s' % args[0]](options=options, args=args)
    except Exception as err:
        print(str(err))

if __name__ == '__main__':
    main()
