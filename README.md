PerfBrowser-CLI
===============

The `pbctl` utility provides a command-line interface to the PerfBrowser
cloud service. 

It allows for:

  * querying and modifying PerfBrowser cloud data via its REST API
  * uploading CSV data derived from performance tools such as `papiex`

The utility is written entirely in `bash`. Its only dependency is `cURL`.

As PerfBrowser cloud implements access control, you will need to sign
up for an account at:

https://perfbrowser.perftools.org

A [demo account](https://perfbrowser.perftools.org/demo) exists to 
try out the service without signing up.

Let's get started!

`pbctl --help` prints a help message detailing its syntax.

The first thing to do once you have a login/password to PerfBrowser
cloud is to login from the command-line. This automatically saves an 
encrypted token on your disk under `$HOME/.perfbrowser`.

      $ pbctl login
      Username or email: test123@example.com
      Password: ********
      Login successful (token saved)

You only need to login once. The saved token will provide secure access
for subsequent operations.

`pbctl` output is in JSON, and can be parsed by a utility like `jq`.

Let's see a jobs listing:

    $ pbctl list
    {
      "jobs": [
        {
          "id": 3,
          "info": {
            "compiler": "gcc/4.3",
            "ncpus": 240,
            "nnodes": 32,
            "study": "NAMD_opt",
            "tags": [
              "harvard",
              "oss"
            ]
          },
          "name": "Gadget",
          "perfdataUrl": "https://perfbrowser.perftools.org/api/1.0/3/perfdata/",
          "resourceUrl": "https://perfbrowser.perftools.org/api/1.0/jobs/3/",
          "userId": 1
        },
        {
          "id": 1,
          "info": {
            "compiler": "gcc/4.3",
            "ncpus": 2,
            "nnodes": 1,
            "study": "NAMD_opt",
            "tags": [
              "yale", 
              "oss"
            ]
          }, 
          "name": "NAMD v1", 
          "perfdataUrl": "https://perfbrowser.perftools.org/api/1.0/1/perfdata/", 
          "resourceUrl": "https://perfbrowser.perftools.org/api/1.0/jobs/1/", 
          "userId": 1
        } 
      ], 
      "userId": 1
    }
    
To query a particular job, you'd do:

    $ pbctl show 1
    {
      "jobId": 1, 
      "perfdata": [
        {
          "collector": "papiex", 
          "data": {
            "cycles": 1100000, 
            "rank": 1
          }, 
          "id": 2, 
          "jobId": 1
        }, 
        {
          "collector": "papiex", 
          "data": {
            "cycles": 1000000, 
            "rank": 0
          }, 
          "id": 1, 
          "jobId": 1
        }
      ]
    }

To upload a CSV file, you can use the `import` argument:

    $ pbctl import test/data/sample.papiex.csv 
    importing test/data/sample.papiex.csv with 240 records.. 
    {
      "id": 4, 
      "info": null, 
      "name": "ONXRFVCHSY", 
      "perfdataUrl": "https://perfbrowser.perftools.org/api/1.0/4/perfdata/", 
      "resourceUrl": "https://perfbrowser.perftools.org/api/1.0/jobs/4/", 
      "userId": 1
    }
    import of test/data/sample.papiex.csv successful


Bugs
----
Your feedback and bug reports are appreciated. Please mail them to:

support@perfbrowser.perftools.org


License
-------
Refer to:

https://perfbrowser.perftools.org/license#cli
