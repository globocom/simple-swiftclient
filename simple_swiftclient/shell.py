#!/usr/bin/python -u
"""
Simple swiftclient to manage objects (v0.0.1 - only upload).

It was based on Openstack python-swiftclient, but using only python standard
libraries.
"""

from __future__ import print_function

from optparse import OptionParser, OptionGroup, SUPPRESS_HELP
from os import environ
from sys import argv as sys_argv, exit

from client import Client


commands = ('upload')


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

    version = '0.0.2'

    parser = OptionParser(version='%%prog %s' % version,
                          usage='''
usage: %%prog [--version] [--help]
             [--os-username <auth-user-name>]
             [--os-password <auth-password>]
             [--os-tenant-name <auth-tenant-name>]
             [--os-auth-url <auth-url>]
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
                      default=environ.get('OS_USERNAME',
                                          environ.get('SWIFT_USER')),
                      help='OpenStack username. Defaults to env[OS_USERNAME].')
    os_grp.add_option('--os_username',
                      help=SUPPRESS_HELP)
    os_grp.add_option('--os-password',
                      metavar='<auth-password>',
                      default=environ.get('OS_PASSWORD',
                                          environ.get('SWIFT_PASSWORD')),
                      help='OpenStack password. Defaults to env[OS_PASSWORD].')
    os_grp.add_option('--os-tenant-name',
                      metavar='<auth-tenant-name>',
                      default=environ.get('OS_TENANT_NAME',
                                          environ.get('SWIFT_TENANT')),
                      help='OpenStack tenant name. '
                           'Defaults to env[OS_TENANT_NAME].')
    os_grp.add_option('--os_tenant_name',
                      help=SUPPRESS_HELP)
    os_grp.add_option('--os-auth-url',
                      metavar='<auth-url>',
                      default=environ.get('OS_AUTH_URL',
                                          environ.get('SWIFT_AUTH_URL')),
                      help='OpenStack auth URL. Defaults to env[OS_AUTH_URL].')
    os_grp.add_option('--os_auth_url',
                      help=SUPPRESS_HELP)
    os_grp.add_option('--os-storage-url',
                      metavar='<storage-url>',
                      default=environ.get('OS_STORAGE_URL',
                                          environ.get('SWIFT_ADMIN_URL')),
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
