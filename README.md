# C-C-C-Combo Breaker!!!

Executes commands with all combinations of supplied arguments.

## Installation
- Clone the repo or download [combobreaker.py](https://raw.githubusercontent.com/qistoph/ComboBreaker/master/combobreaker.py).
- Make it executable `chmod +x combobreaker.py`
- To make cmbrk available system wide:
  - `sudo cp combobreaker.py /usr/local/bin/cmbrk`
  - `chmod 755 /usr/local/bin/cmbrk`

## Simple example
```
$ cmbrk echo [ Hi Hello Hey ] [ Alex Bert Chris ]
Hi Alex
Hi Bert
Hi Chris
Hello Alex
Hello Bert
Hello Chris
Hey Alex
Hey Bert
Hey Chris
```

Arguments:
- `echo` The command tool to use
- `[ Hi Hello Hey ]` Possibilities for first argument are "Hi", "Hello" and "Hey"
- `[ Alex Bert Chris ]` Options for the second argument

## Nested example
```
$ cmbrk -v touch [ -[ dirs.txt ] / [ file1 file2 file 3] ]
exec: touch dir1/file1
exec: touch dir1/file2
exec: touch dir1/file3
exec: touch dir2/file1
exec: touch dir2/file2
exec: touch dir2/file3
exec: touch dir3/file1
exec: touch dir3/file2
exec: touch dir3/file3
```

Arguments:
- `-v` Increase verbosity to 1 to show commands executed
- `touch` The command to run
- `[ ... ]` Nested arguments, they will be combined without spaces
- `-[ dirs.txt ]` Read these arguments from the file `dirs.txt`
- `/` Add a `/` between the dir and file
- `[ file1 file2 file3 ]` Files to create in each directory

## Complex example
Find a valid match of an RSA private key, encrypted packet and its padding.

```
$ ls
data0.enc  data4.enc  data8.enc     private2.pem  private6.pem
data1.enc  data5.enc  data9.enc     private3.pem  private7.pem
data2.enc  data6.enc  private0.pem  private4.pem  private8.pem
data3.enc  data7.enc  private1.pem  private5.pem  private9.pem

$ cmbrk -c -v -ss -z openssl rsautl -inkey [ private*.pem ] -decrypt -in [ data*.enc ] [ -ssl -pkcs -oaep -x931 ]
Executing 400 commands in 3  2  1  ...
[ ... omitted for brevity ]
exec: openssl rsautl -inkey private2.pem -decrypt -in data6.enc -pkcs
exec: openssl rsautl -inkey private2.pem -decrypt -in data6.enc -oaep
Some message

C-C-C-Combo Breaker! Exit code is 0.
openssl rsautl -inkey private2.pem -decrypt -in data6.enc -oaep
```

Arguments:
- `-c` Count the total number of combinations, and show countdown
- `-v` Increase verbosity to 1 to show commands executed
- `-ss` Silence stderr
- `-z` Stop executing commands when a command exits with code 0
- `openssl rsautl` Call the RSA utility in OpenSSL
- `-inkey` Following argument will be the key to use
- `[ private*.pem ]` This will be expanded by your shell (bash) to all matching files
- `-decrypt` Instruction to decrypt
- `-in` Following argument will be the file to decrypt
- `[ data*.enc ]` Expanded by shell to all data files
- `[ -ssl -pkcs -oaep -x931 ]` Different padding options to try

## Usage
```
usage: cmbrk [options] <command> [args]

Combinations of arguments between [ and ] will be iterated.
Note that spaces around the brackets are mandatory. Some examples:
cmbrk echo [ Hi Hello ] [ Alex Bob ]
Hi Alex
Hi Bob
Hello Alex
Hello Bob

Use -[ files ... ] to read arguments from specified file(s), e.g.:
cmbrk echo -[ saluts.txt ] -[ names.txt ]

Nested args are combined into 1 argument, e.g.:
cmbrk touch [ [ dir1 dir2 dir3 ] / [ file1 file2 file3 ] ]
Creates dir1/file1, dir1/file2, dir1/file3 etc

options:
  -h, --help            show this help message and exit
  -v, --verbose         Increase verbosity, use multiple times to increase
                        more (-vv)
  -s, --silent          Silence stdout of called command. -ss silences stderr
                        and -sss silences both
  -c, --count           Show number of commands before executing. Number of
                        combinations can grow really fast. This allows you to
                        reconsider before actually starting
  -z, --zero            Break execution on first 0 exit code
  -Z, --notzero         Break execution on first none 0 exit code
  -m MATCH, --match MATCH
                        Break execution when stdout matches MATCH
  -M MATCH, --nomatch MATCH
                        Break execution when stdout doesn't match MATCH
```
