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

import signal
# import socket
# import logging

from optparse import OptionParser, OptionGroup, SUPPRESS_HELP
from os import environ, _exit as os_exit
# from os.path import isfile, isdir, join
from sys import argv as sys_argv, exit, stderr
# from time import gmtime, strftime

commands = ('upload')
# commands = ('delete', 'download', 'list', 'post',
#             'stat', 'upload', 'capabilities', 'info', 'tempurl')


def immediate_exit(signum, frame):
    stderr.write(" Aborted\n")
    os_exit(2)

# st_delete_options = '''[-all] [--leave-segments]
#                     [--object-threads <threads>]
#                     [--container-threads <threads>]
#                     <container> [object]
# '''

# st_delete_help = '''
# Delete a container or objects within a container.

# Positional arguments:
#   <container>           Name of container to delete from.
#   [object]              Name of object to delete. Specify multiple times
#                         for multiple objects.

# Optional arguments:
#   --all                 Delete all containers and objects.
#   --leave-segments      Do not delete segments of manifest objects.
#   --object-threads <threads>
#                         Number of threads to use for deleting objects.
#                         Default is 10.
#   --container-threads <threads>
#                         Number of threads to use for deleting containers.
#                         Default is 10.
# '''.strip("\n")


# def st_delete(parser, args, output_manager):
#     parser.add_option(
#         '-a', '--all', action='store_true', dest='yes_all',
#         default=False, help='Delete all containers and objects.')
#     parser.add_option(
#         '', '--leave-segments', action='store_true',
#         dest='leave_segments', default=False,
#         help='Do not delete segments of manifest objects.')
#     parser.add_option(
#         '', '--object-threads', type=int,
#         default=10, help='Number of threads to use for deleting objects. '
#         'Default is 10.')
#     parser.add_option('', '--container-threads', type=int,
#                       default=10, help='Number of threads to use for '
#                       'deleting containers. '
#                       'Default is 10.')
#     (options, args) = parse_args(parser, args)


# st_download_options = '''[--all] [--marker] [--prefix <prefix>]
#                       [--output <out_file>] [--object-threads <threads>]
#                       [--container-threads <threads>] [--no-download]
#                       [--skip-identical] <container> <object>
# '''

# st_download_help = '''
# Download objects from containers.

# Positional arguments:
#   <container>           Name of container to download from. To download a
#                         whole account, omit this and specify --all.
#   <object>              Name of object to download. Specify multiple times
#                         for multiple objects. Omit this to download all
#                         objects from the container.

# Optional arguments:
#   --all                 Indicates that you really want to download
#                         everything in the account.
#   --marker              Marker to use when starting a container or account
#                         download.
#   --prefix <prefix>     Only download items beginning with <prefix>
#   --output <out_file>   For a single file download, stream the output to
#                         <out_file>. Specifying "-" as <out_file> will
#                         redirect to stdout.
#   --object-threads <threads>
#                         Number of threads to use for downloading objects.
#                         Default is 10.
#   --container-threads <threads>
#                         Number of threads to use for downloading containers.
#                         Default is 10.
#   --no-download         Perform download(s), but don't actually write anything
#                         to disk.
#   --header <header_name:header_value>
#                         Adds a customized request header to the query, like
#                         "Range" or "If-Match". This argument is repeatable.
#                         Example --header "content-type:text/plain"
#   --skip-identical      Skip downloading files that are identical on both
#                         sides.
# '''.strip("\n")


# def st_download(parser, args, output_manager):
#     parser.add_option(
#         '-a', '--all', action='store_true', dest='yes_all',
#         default=False, help='Indicates that you really want to download '
#         'everything in the account.')
#     parser.add_option(
#         '-m', '--marker', dest='marker',
#         default='', help='Marker to use when starting a container or '
#         'account download.')
#     parser.add_option(
#         '-p', '--prefix', dest='prefix',
#         help='Only download items beginning with the <prefix>.')
#     parser.add_option(
#         '-o', '--output', dest='out_file', help='For a single '
#         'download, stream the output to <out_file>. '
#         'Specifying "-" as <out_file> will redirect to stdout.')
#     parser.add_option(
#         '', '--object-threads', type=int,
#         default=10, help='Number of threads to use for downloading objects. '
#         'Default is 10.')
#     parser.add_option(
#         '', '--container-threads', type=int, default=10,
#         help='Number of threads to use for downloading containers. '
#         'Default is 10.')
#     parser.add_option(
#         '', '--no-download', action='store_true',
#         default=False,
#         help="Perform download(s), but don't actually write anything to disk.")
#     parser.add_option(
#         '-H', '--header', action='append', dest='header',
#         default=[],
#         help='Adds a customized request header to the query, like "Range" or '
#         '"If-Match". This argument is repeatable. '
#         'Example: --header "content-type:text/plain"')
#     parser.add_option(
#         '--skip-identical', action='store_true', dest='skip_identical',
#         default=False, help='Skip downloading files that are identical on '
#         'both sides.')
#     (options, args) = parse_args(parser, args)


# st_list_options = '''[--long] [--lh] [--totals] [--prefix <prefix>]
#                   [--delimiter <delimiter>]
# '''

# st_list_help = '''
# Lists the containers for the account or the objects for a container.

# Positional arguments:
#   [container]           Name of container to list object in.

# Optional arguments:
#   --long                Long listing format, similar to ls -l.
#   --lh                  Report sizes in human readable format similar to
#                         ls -lh.
#   --totals              Used with -l or --lh, only report totals.
#   --prefix              Only list items beginning with the prefix.
#   --delimiter           Roll up items with the given delimiter. For containers
#                         only. See OpenStack Swift API documentation for what
#                         this means.
# '''.strip('\n')


# def st_list(parser, args, output_manager):
#     parser.add_option(
#         '-l', '--long', dest='long', action='store_true', default=False,
#         help='Long listing format, similar to ls -l.')
#     parser.add_option(
#         '--lh', dest='human', action='store_true',
#         default=False, help='Report sizes in human readable format, '
#         "similar to ls -lh.")
#     parser.add_option(
#         '-t', '--totals', dest='totals',
#         help='used with -l or --lh, only report totals.',
#         action='store_true', default=False)
#     parser.add_option(
#         '-p', '--prefix', dest='prefix',
#         help='Only list items beginning with the prefix.')
#     parser.add_option(
#         '-d', '--delimiter', dest='delimiter',
#         help='Roll up items with the given delimiter. For containers '
#              'only. See OpenStack Swift API documentation for '
#              'what this means.')
#     (options, args) = parse_args(parser, args)


# st_stat_options = '''[--lh]
#                   [container] [object]
# '''

# st_stat_help = '''
# Displays information for the account, container, or object.

# Positional arguments:
#   [container]           Name of container to stat from.
#   [object]              Name of object to stat.

# Optional arguments:
#   --lh                  Report sizes in human readable format similar to
#                         ls -lh.
# '''.strip('\n')


# def st_stat(parser, args, output_manager):
#     parser.add_option(
#         '--lh', dest='human', action='store_true', default=False,
#         help='Report sizes in human readable format similar to ls -lh.')
#     (options, args) = parse_args(parser, args)


# st_post_options = '''[--read-acl <acl>] [--write-acl <acl>] [--sync-to]
#                   [--sync-key <sync-key>] [--meta <name:value>]
#                   [--header <header>]
#                   [container] [object]
# '''

# st_post_help = '''
# Updates meta information for the account, container, or object.
# If the container is not found, it will be created automatically.

# Positional arguments:
#   [container]           Name of container to post to.
#   [object]              Name of object to post.

# Optional arguments:
#   --read-acl <acl>      Read ACL for containers. Quick summary of ACL syntax:
#                         .r:*, .r:-.example.com, .r:www.example.com, account1,
#                         account2:user2
#   --write-acl <acl>     Write ACL for containers. Quick summary of ACL syntax:
#                         account1 account2:user2
#   --sync-to <sync-to>   Sync To for containers, for multi-cluster replication.
#   --sync-key <sync-key> Sync Key for containers, for multi-cluster replication.
#   --meta <name:value>   Sets a meta data item. This option may be repeated.
#                         Example: -m Color:Blue -m Size:Large
#   --header <header>     Set request headers. This option may be repeated.
#                         Example -H "content-type:text/plain"
# '''.strip('\n')


# def st_post(parser, args, output_manager):
#     parser.add_option(
#         '-r', '--read-acl', dest='read_acl', help='Read ACL for containers. '
#         'Quick summary of ACL syntax: .r:*, .r:-.example.com, '
#         '.r:www.example.com, account1, account2:user2')
#     parser.add_option(
#         '-w', '--write-acl', dest='write_acl', help='Write ACL for '
#         'containers. Quick summary of ACL syntax: account1, '
#         'account2:user2')
#     parser.add_option(
#         '-t', '--sync-to', dest='sync_to', help='Sets the '
#         'Sync To for containers, for multi-cluster replication.')
#     parser.add_option(
#         '-k', '--sync-key', dest='sync_key', help='Sets the '
#         'Sync Key for containers, for multi-cluster replication.')
#     parser.add_option(
#         '-m', '--meta', action='append', dest='meta', default=[],
#         help='Sets a meta data item. This option may be repeated. '
#         'Example: -m Color:Blue -m Size:Large')
#     parser.add_option(
#         '-H', '--header', action='append', dest='header',
#         default=[], help='Set request headers. This option may be repeated. '
#         'Example: -H "content-type:text/plain" '
#         '-H "Content-Length: 4000"')
#     (options, args) = parse_args(parser, args)


# st_upload_options = '''[--changed] [--skip-identical] [--segment-size <size>]
#                     [--segment-container <container>] [--leave-segments]
#                     [--object-threads <thread>] [--segment-threads <threads>]
#                     [--header <header>] [--use-slo]
#                     [--object-name <object-name>]
#                     <container> <file_or_directory>
# '''

# st_upload_help = '''
# Uploads specified files and directories to the given container.

# Positional arguments:
#   <container>           Name of container to upload to.
#   <file_or_directory>   Name of file or directory to upload. Specify multiple
#                         times for multiple uploads.

# Optional arguments:
#   --changed             Only upload files that have changed since the last
#                         upload.
#   --skip-identical      Skip uploading files that are identical on both sides.
#   --segment-size <size> Upload files in segments no larger than <size> (in
#                         Bytes) and then create a "manifest" file that will
#                         download all the segments as if it were the original
#                         file.
#   --segment-container <container>
#                         Upload the segments into the specified container. If
#                         not specified, the segments will be uploaded to a
#                         <container>_segments container to not pollute the
#                         main <container> listings.
#   --leave-segments      Indicates that you want the older segments of manifest
#                         objects left alone (in the case of overwrites).
#   --object-threads <threads>
#                         Number of threads to use for uploading full objects.
#                         Default is 10.
#   --segment-threads <threads>
#                         Number of threads to use for uploading object segments.
#                         Default is 10.
#   --header <header>     Set request headers with the syntax header:value.
#                         This option may be repeated.
#                         Example -H "content-type:text/plain".
#   --use-slo             When used in conjunction with --segment-size it will
#                         create a Static Large Object instead of the default
#                         Dynamic Large Object.
#   --object-name <object-name>
#                         Upload file and name object to <object-name> or upload
#                         dir and use <object-name> as object prefix instead of
#                         folder name.
# '''.strip('\n')


def st_upload(options):

    values = {
        'username': options.os_username,
        'password': options.os_password,
        'auth_url': options.os_auth_url,
        'tenant_name': options.os_tenant_name,
    }

    pass
#     parser.add_option(
#         '-c', '--changed', action='store_true', dest='changed',
#         default=False, help='Only upload files that have changed since '
#         'the last upload.')
#     parser.add_option(
#         '--skip-identical', action='store_true', dest='skip_identical',
#         default=False, help='Skip uploading files that are identical on '
#         'both sides.')
#     parser.add_option(
#         '-S', '--segment-size', dest='segment_size', help='Upload files '
#         'in segments no larger than <size> (in Bytes) and then create a '
#         '"manifest" file that will download all the segments as if it were '
#         'the original file. Sizes may also be expressed as bytes with the '
#         'B suffix, kilobytes with the K suffix, megabytes with the M suffix '
#         'or gigabytes with the G suffix.')
#     parser.add_option(
#         '-C', '--segment-container', dest='segment_container',
#         help='Upload the segments into the specified container. '
#         'If not specified, the segments will be uploaded to a '
#         '<container>_segments container to not pollute the main '
#         '<container> listings.')
#     parser.add_option(
#         '', '--leave-segments', action='store_true',
#         dest='leave_segments', default=False, help='Indicates that you want '
#         'the older segments of manifest objects left alone (in the case of '
#         'overwrites).')
#     parser.add_option(
#         '', '--object-threads', type=int, default=10,
#         help='Number of threads to use for uploading full objects. '
#         'Default is 10.')
#     parser.add_option(
#         '', '--segment-threads', type=int, default=10,
#         help='Number of threads to use for uploading object segments. '
#         'Default is 10.')
#     parser.add_option(
#         '-H', '--header', action='append', dest='header',
#         default=[], help='Set request headers with the syntax header:value. '
#         ' This option may be repeated. Example -H "content-type:text/plain" '
#         '-H "Content-Length: 4000"')
#     parser.add_option(
#         '', '--use-slo', action='store_true', default=False,
#         help='When used in conjunction with --segment-size, it will '
#         'create a Static Large Object instead of the default '
#         'Dynamic Large Object.')
#     parser.add_option(
#         '', '--object-name', dest='object_name',
#         help='Upload file and name object to <object-name> or upload dir and '
#         'use <object-name> as object prefix instead of folder name.')
#     (options, args) = parse_args(parser, args)


# st_capabilities_options = "[<proxy_url>]"
# st_info_options = st_capabilities_options
# st_capabilities_help = '''
# Retrieve capability of the proxy.

# Optional positional arguments:
#   <proxy_url>           Proxy URL of the cluster to retrieve capabilities.
# '''.strip('\n')
# st_info_help = st_capabilities_help


# def st_capabilities(parser, args, output_manager):
#     def _print_compo_cap(name, capabilities):
#         for feature, options in sorted(capabilities.items(),
#                                        key=lambda x: x[0]):
#             output_manager.print_msg("%s: %s" % (name, feature))
#             if options:
#                 output_manager.print_msg(" Options:")
#                 for key, value in sorted(options.items(),
#                                          key=lambda x: x[0]):
#                     output_manager.print_msg("  %s: %s" % (key, value))

#     (options, args) = parse_args(parser, args)

# st_info = st_capabilities


# st_tempurl_options = '<method> <seconds> <path> <key>'


# st_tempurl_help = '''
# Generates a temporary URL for a Swift object.

# Positions arguments:
#   [method]              An HTTP method to allow for this temporary URL.
#                         Usually 'GET' or 'PUT'.
#   [seconds]             The amount of time in seconds the temporary URL will
#                         be valid for.
#   [path]                The full path to the Swift object. Example:
#                         /v1/AUTH_account/c/o.
#   [key]                 The secret temporary URL key set on the Swift cluster.
#                         To set a key, run \'swift post -m
#                         "Temp-URL-Key:b3968d0207b54ece87cccc06515a89d4"\'
# '''.strip('\n')


# def st_tempurl(parser, args, thread_manager):
#     (options, args) = parse_args(parser, args)
#     args = args[1:]
#     if len(args) < 4:
#         thread_manager.error('Usage: %s tempurl %s\n%s', BASENAME,
#                              st_tempurl_options, st_tempurl_help)
#         return
#     method, seconds, path, key = args[:4]
#     try:
#         seconds = int(seconds)
#     except ValueError:
#         thread_manager.error('Seconds must be an integer')
#         return
#     if method.upper() not in ['GET', 'PUT', 'HEAD', 'POST', 'DELETE']:
#         thread_manager.print_msg('WARNING: Non default HTTP method %s for '
#                                  'tempurl specified, possibly an error' %
#                                  method.upper())
#     url = generate_temp_url(path, seconds, key, method)
#     thread_manager.print_msg(url)


# def parse_args(parser, args, enforce_requires=True):
#     if not args:
#         args = ['-h']
#     (options, args) = parser.parse_args(args)

#     if len(args) > 1 and args[1] == '--help':
#         _help = globals().get('st_%s_help' % args[0],
#                               "no help for %s" % args[0])
#         print(_help)
#         exit()

#     # Short circuit for tempurl, which doesn't need auth
#     if len(args) > 0 and args[0] == 'tempurl':
#         return options, args

#     if options.auth_version == '3.0':
#         # tolerate sloppy auth_version
#         options.auth_version = '3'

#     if (not (options.auth and options.user and options.key)
#             and options.auth_version != '3'):
#         # Use keystone auth if any of the old-style args are missing
#         options.auth_version = '2.0'

#     # Use new-style args if old ones not present
#     if not options.auth and options.os_auth_url:
#         options.auth = options.os_auth_url
#     if not options.user and options.os_username:
#         options.user = options.os_username

#     # Specific OpenStack options
#     options.os_options = {
#         'tenant_name': options.os_tenant_name,
#         'object_storage_url': options.os_storage_url,
#     }

#     if len(args) > 1 and args[0] == "capabilities":
#         return options, args

#     if (options.os_options.get('object_storage_url') and
#             options.os_options.get('auth_token') and
#             (options.auth_version == '2.0' or options.auth_version == '3')):
#         return options, args

#     if enforce_requires:
#         if options.auth_version == '3':
#             if not options.auth:
#                 exit('Auth version 3 requires OS_AUTH_URL to be set or ' +
#                      'overridden with --os-auth-url')
#             if not (options.user or options.os_user_id):
#                 exit('Auth version 3 requires either OS_USERNAME or ' +
#                      'OS_USER_ID to be set or overridden with ' +
#                      '--os-username or --os-user-id respectively.')
#             if not options.key:
#                 exit('Auth version 3 requires OS_PASSWORD to be set or ' +
#                      'overridden with --os-password')
#         elif not (options.auth and options.user and options.key):
#             exit('''
# Auth version 1.0 requires ST_AUTH, ST_USER, and ST_KEY environment variables
# to be set or overridden with -A, -U, or -K.

# Auth version 2.0 requires OS_AUTH_URL, OS_USERNAME, OS_PASSWORD, and
# OS_TENANT_NAME OS_TENANT_ID to be set or overridden with --os-auth-url,
# --os-username, --os-password, --os-tenant-name or os-tenant-id. Note:
# adding "-V 2" is necessary for this.'''.strip('\n'))
#     return options, args


def main(arguments=None):
    if arguments:
        argv = arguments
    else:
        argv = sys_argv

    version = '1.0'
    parser = OptionParser(version='%%prog %s' % version,
                          usage='''
usage: %%prog [--version] [--help]
             [--auth <auth_url>]
             [--auth-version <auth_version>] [--user <username>]
             [--os-username <auth-user-name>] [--os-password <auth-password>]
             [--os-tenant-name <auth-tenant-name>]
             [--os-auth-url <auth-url>] [--os-auth-token <auth-token>]
             [--os-storage-url <storage-url>] [--os-region-name <region-name>]
             <subcommand> [--help]

Command-line interface to the OpenStack Swift API.

Positional arguments:
  <subcommand>
    upload               Uploads files or directories to the given container.

  %%prog list --lh
# '''.strip('\n') % globals())
    parser.add_option('-V', '--auth-version',
                      dest='auth_version',
                      default=environ.get('ST_AUTH_VERSION',
                                          (environ.get('OS_AUTH_VERSION',
                                                       '1.0'))),
                      type=str,
                      help='Specify a version for authentication. '
                           'Defaults to 1.0.')
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
        globals()['st_%s' % args[0]](options=options)
    except Exception as err:
        print(str(err))

if __name__ == '__main__':
    main()
