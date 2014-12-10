A simple Openstack Swift Client to manage objects using python standard libraries. No extra packages required.

## Why not just use Openstack python-swiftclient?

Openstack python-swiftclient requires extra packages to work properly. As long as this script was originally created to upload static files on Tsuru deploy process, we needed a light way to upload files.

# Install

	pip install simple-swiftclient 

# Usage

## Uploading files

```
simpleswift --os-auth-url <https://yourhost:5000/v2.0> --os-username <username> --os-password <password> --os-tenant-name <tenant name> upload <container name> <file|directory>
```

- file: upload a single file
- directory: upload all files found in all directories

### Objects name convention

Given this directory structure:

```
static
|-- css
|    |-- base.css 
|-- js
|    |-- main.js 
```

Example 1:

	$ simpleswift [...] upload <container> static/css/base.css
	
This will create an object named **static/css/base.css**

See [Pseudo-hierarchical folders and directories](http://docs.openstack.org/api/openstack-object-storage/1.0/content/pseudo-hierarchical-folders-directories.html)

Example 2:

	$ simpleswift [...] upload <container> static/
	
This will create 2 objects named **static/css/base.css** and **static/js/main.js**

Example 3:

```
$ cd static/css
$ simpleswift [...] upload <container> base.css
```
	
This will create an object named **base.css**
