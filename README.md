# C-C-C-Combo Breaker!!!

Executes commands with all combinations of supplied arguments.

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

Combinations of arguments between [ and ] will be executed, e.g.:

cmbrk echo [ Hi Hello ] [ Alex Bob ]
Hi Alex
Hi Bob
Hello Alex
Hello Bob

Use -[ files ... ] to read arguments from specified file(s)

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
                        Break execution when stdout matches MATACH
  -M MATCH, --nomatch MATCH
                        Break execution when stdout doesn't match MATACH
```
