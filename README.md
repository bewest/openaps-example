# openaps-example
WORK IN PROGRESS example instance of openaps
This is kind of a kitchen sink show case/demonstration of openaps capabilities.
See the [history](https://github.com/bewest/openaps-example/commits/master)
for a complete accounting of the commands used.

##  using a commandline script as device plugin

The new `process` vendor:
Let's say you have a `node` js script called `iob.js`:

    openaps device add calciob process --require input node iob.js

Which says: create a **device** implemented by openaps **vendor**
`process`, called `calciob` which runs the script
`node iob.js` and has one argument, we'll refer to as `input` Then
`openaps use --format text calciob shell pump-history.json` or
similar can be used to try it out.

```bash
bewest@hither:~/Documents/foo$
 $ openaps use --format text calciob shell pump-history.json 
{"iob":1.4710394611199997,"activity":0.04893333333333332}
bewest@hither:~/Documents/foo$
```

When comfy, save the report configuration with:

    openaps report add iob.json text calciob shell pump-history.json

which says: create a **report** called `iob.json`, which is the
_usage_ of **device** `calciob`, _usage_ `shell`, (which is running
`node iob.js`) with the argument `pump-history.json`... Since this
node script happens to always print json, we're using the `text` output
to save it as-is:

```bash
$ openaps report  invoke  iob.json 
calciob://text/shell/iob.json
reporting iob.json
```

so now it supports python python plugins plus arbitrary commands 
this is what my openaps use menu looks like now:
```bash
$ openaps use -h
usage: openaps-use [-h] [--format {text,json,base,stdout}] [--output OUTPUT]
                   [--version]
                   {agp,calciob,cgm,pump} ...

 openaps-use - use a registered device

positional arguments:
  {agp,calciob,cgm,pump}
                        Operation
    agp                 AGP - calculate agp values given some glucose text
    calciob             process - a fake vendor to run arbitrary commands
    cgm                 Dexcom - openaps driver for dexcom
    pump                Medtronic - openaps driver for Medtronic
```

```bash
$ openaps use calciob -h
usage: openaps-use calciob [-h] {shell} ...

positional arguments:
  {shell}     Operation
    shell     run a process in a subshell

optional arguments:
  -h, --help  show this help message and exit
```

We can see that the `input` argument is also expected.

```bash
$ openaps use calciob -h
usage: openaps-use calciob shell [-h] input

positional arguments:
  input

optional arguments:
  -h, --help  show this help message and exit
```


### Custom python plugins

See [agp plugin by @mgranberry](https://gist.github.com/mgranberry/afde7373ed756e538dad),
and my [agp openaps plugin
version](https://github.com/bewest/openaps-example/blob/master/agp.py)

Once it's a subclass of `openaps.uses.use.Use`, openaps can use it:

```bash
$ openaps vendor -h
usage: openaps-vendor [-h] {add,remove,show} ...

  openaps-vendor - Manage vendor plugins.

positional arguments:
  {add,remove,show}  Operation
    add              Add a new vendor plugin to openaps-environment.
    remove           Remove vendor plugin from openaps-environment
    show             Show/list vendor plugins

optional arguments:
  -h, --help         show this help message and exit

show    - lists all known vendors
add     - add a new vendor
remove  - remove a vendor
```


```bash
$ openaps vendor add -h
usage: openaps-vendor add [-h] [--path PATH] name

positional arguments:
  name

optional arguments:
  -h, --help   show this help message and exit
  --path PATH  Path to module's namespace
```

It knows if it's not a python module:

```bash
$ openaps vendor add not-a-real-module
No module named not-a-real-module
not-a-real-module doesn't seem to be an importable python module
If it is a python module, try using --path to influence
PYTHONPATH
      
```

```bash
$ ls agp.py
+ ls agp.py
agp.py
$ openaps vendor add agp
added agp://
```

Now it's available in the devices menu:

```
+ openaps device add -h
usage: openaps-device add [-h] name {dexcom,medtronic,process,agp} ...

positional arguments:
  name
  {dexcom,medtronic,process,agp}
                        Operation
    dexcom              Dexcom - openaps driver for dexcom
    medtronic           Medtronic - openaps driver for Medtronic
    process             process - a fake vendor to run arbitrary commands
    agp                 AGP - calculate agp values given some glucose text

optional arguments:
  -h, --help            show this help message and exit
```


Add device:

```bash
+ openaps device add my-agp agp -h
usage: openaps-device add name agp [-h]

optional arguments:
  -h, --help  show this help message and exit

+ openaps device add my-agp agp
added agp://my-agp
```

Now we can **use** it.

## `openaps use`!

```bash
+ openaps use -h
usage: openaps-use [-h] [--format {text,json,base,stdout}] [--output OUTPUT]
                   [--version]
                   {agp,calciob,cgm,my-agp,pump} ...

 openaps-use - use a registered device

positional arguments:
  {agp,calciob,cgm,my-agp,pump}
                        Operation
    agp                 AGP - calculate agp values given some glucose text
    calciob             process - a fake vendor to run arbitrary commands
    cgm                 Dexcom - openaps driver for dexcom
    my-agp              AGP - calculate agp values given some glucose text
    pump                Medtronic - openaps driver for Medtronic

optional arguments:
  -h, --help            show this help message and exit
  --format {text,json,base,stdout}
  --output OUTPUT
  --version             show program's version number and exit

Once a device is registered in openaps.ini, it can be used.
```

Let's try the agp:

```bash

+ openaps use my-agp -h
usage: openaps-use my-agp [-h] {agp} ...

positional arguments:
  {agp}       Operation
    agp       Calculate agp

optional arguments:
  -h, --help  show this help message and exit
```

It even has it's own usage:
```bash
+ openaps use my-agp agp -h
usage: openaps-use my-agp agp [-h] input

positional arguments:
  input

optional arguments:
  -h, --help  show this help message and exit
```

Demonstrate usage:

```
+ openaps use --format text my-agp agp glucose.txt
[(0, (86, 121, 156, 222, 392)), (1, (39, 137, 155, 249, 318)), (2, (72, 124, 167, 247, 302)), (3, (97, 121, 168, 252, 339)), (4, (102, 143, 189, 241, 338)), (5, (103, 144, 171, 211, 327)), (6, (104, 157, 169, 204, 304)), (7, (103, 137, 185, 212, 302)), (8, (87, 95, 200, 252, 323)), (9, (74, 108, 195, 256, 278)), (10, (62, 103, 173, 241, 251)), (11, (100, 150, 171, 224, 250)), (12, (94, 132, 154, 194, 307)), (13, (76, 112, 141, 202, 248)), (14, (76, 100, 133, 180, 235)), (15, (77, 94, 121, 146, 197)), (16, (70, 78, 118, 150, 173)), (17, (61, 90, 114, 148, 163)), (18, (85, 93, 123, 152, 161)), (19, (65, 86, 121, 138, 199)), (20, (51, 67, 103, 117, 296)), (21, (39, 84, 99, 147, 289)), (22, (59, 83, 109, 165, 214)), (23, (87, 98, 131, 157, 304))]
```

