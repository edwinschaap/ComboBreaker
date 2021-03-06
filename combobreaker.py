#!/usr/bin/python3

import re
import sys
import argparse
import subprocess
from time import sleep
from functools import reduce
from operator import mul

class GroupingException(Exception):
    pass

def getArgsFromFile(filename):
    f = open(filename, 'r')
    lines = [l.strip() for l in f]
    return lines

def listGroups(cmds, d=0):
    #print('listGroups(', cmds, ')')
    i = 0
    depth = 0
    start = -1
    fromFile = False
    hasNested = False
    while i < len(cmds):
        if cmds[i] == '[' or cmds[i] == "-[":
            if depth == 0:
                start = i
                fromFile = cmds[i] == "-["
            else:
                hasNested = True
            depth += 1
        if cmds[i] == ']':
            depth -= 1
            if depth < 0: raise GroupingException('Unmatched ] at {:d}'.format(i))
            if depth == 0:
                #print('[ ] match {:d}, {:d}'.format(start, i))
                sub = listGroups(cmds[start+1:i], d+1)
                if fromFile:
                    sub = [line for f in sub for line in getArgsFromFile(f)]
                if d == 0 and hasNested:
                    sub = ["".join(g) for g in generator(sub)]
                cmds[start:i+1] = [sub]
                #print(cmds)
                i = start
        #print("  "*d, "i:", i)
        i += 1

    if depth > 0: raise GroupingException('Unmatched [ at {:d}'.format(start))
    return cmds

def parseCmdArguments():
    parser = argparse.ArgumentParser()
    parser.formatter_class=argparse.RawDescriptionHelpFormatter
    parser.usage = '%(prog)s [options] <command> [args]'
    parser.description = 'Combinations of arguments between [ and ] will be iterated.\nNote that spaces around the brackets are mandatory. Some examples:\n' +\
        '%(prog)s echo [ Hi Hello ] [ Alex Bob ]\n' +\
        'Hi Alex\nHi Bob\nHello Alex\nHello Bob\n\n' +\
        'Use -[ files ... ] to read arguments from specified file(s), e.g.:\n' +\
        '%(prog)s echo -[ saluts.txt ] -[ names.txt ]\n\n' +\
        'Nested args are combined into 1 argument, e.g.:\n' +\
        '%(prog)s touch [ [ dir1 dir2 dir3 ] / [ file1 file2 file3 ] ]\n' +\
        'Creates dir1/file1, dir1/file2, dir1/file3 etc\n'
    parser._optionals.title = 'options'

    parser.add_argument('-v', '--verbose', action='count',
        help='Increase verbosity, use multiple times to increase more (-vv)')
    parser.add_argument('-s', '--silent', action='count', default=0,
        help='Silence stdout of called command. -ss silences stderr and -sss silences both')
    parser.add_argument('-c', '--count', action='store_true', default=False,
        help='Show number of commands before executing. Number of combinations can grow really fast. This allows you to reconsider before actually starting')
    parser.add_argument('-z', '--zero', action='store_true',
        help='Break execution on first 0 exit code')
    parser.add_argument('-Z', '--notzero', action='store_true',
        help='Break execution on first none 0 exit code')
    parser.add_argument('-m', '--match', type=str, action='append', default=[],
        help='Break execution if stdout matches MATCH')
    parser.add_argument('-M', '--nomatch', type=str, action='append', metavar='MATCH', default=[],
        help='Break execution if stdout doesn\'t match MATCH')
    parser.add_argument('-r', '--regex', type=str, action='append', metavar='REGEX', default=[],
        help='Break execution if stdout matches REGEX (case insens.)')
    parser.add_argument('-R', '--noregex', type=str, action='append', metavar='REGEX', default=[],
        help='Break execution if stdout doesn\'t match REGEX (case insens.)')
    parser.add_argument('cmd_args', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    args = vars(parser.parse_args())
    if '--' in args['cmd_args']: args['cmd_args'].remove('--')

    #print(args['cmd_args'])
    args['cmd_args'] = listGroups(args['cmd_args'])

    return args   

def generator(fields, d=0):
    for i in range(len(fields)):
        field = fields[i]
        if isinstance(field, list):
            for value in field:
                cmd = fields[:]
                cmd[i] = value
                for ans in generator(cmd, d+1):
                    yield ans
            return # Any following args are handled in the generator call

    yield fields

def verbose(text, level=1):
    if options['verbose'] and level <= options['verbose']:
        print(text)

def anyMatch(text, matches):
    for m in matches:
        if m.encode('utf-8') in text:
            return True
    return False

def allMatch(text, matches):
    for m in matches:
        if m.encode('utf-8') not in text:
            return False
    return True

def anyRegex(text, regexes):
    for r in regexes:
        if len(re.findall(r.encode('utf-8'), text), re.IGNORECASE) > 0:
            return True
    return False

def allRegex(text, regexes):
    for r in regexes:
        if len(re.findall(r.encode('utf-8'), text), re.IGNORECASE) == 0:
            return False
    return True

if __name__ == '__main__':
    options = parseCmdArguments()
    #print(options)

    if options['count']:
        countCmds = reduce(mul, [len(i) for i in options['cmd_args'] if isinstance(i, list)])
        sys.stdout.write("Executing {:d} commands in ".format(countCmds))
        for i in range(3, 0, -1):
            sys.stdout.write("{:d}  ".format(i))
            sys.stdout.flush()
            sleep(1)
        sys.stdout.write("\n")
        sys.stdout.flush()

    combobreaker = None
    
    for cmd in generator(options['cmd_args']):
        verbose("exec: " + " ".join(cmd))

        p =subprocess.Popen(" ".join(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if options['silent'] & 1 == 0:
            sys.stdout.buffer.write(out)
            sys.stdout.buffer.flush()
        if options['silent'] & 2 == 0:
            sys.stderr.buffer.write(err)
            sys.stderr.buffer.flush()
        ret = p.returncode

        verbose("Exit code {:d}\n".format(ret), 2)

        if ret == 0 and options['zero']:
            combobreaker = "C-C-C-Combo Breaker! Exit code is 0."
            break
        if ret != 0 and options['notzero']:
            combobreaker = "C-C-C-Combo Breaker! Exit code is not 0."
            break
        if anyMatch(out, options['match']):
            combobreaker = "C-C-C-Combo Breaker! Output matched."
            break
        if not allMatch(out, options['nomatch']):
            combobreaker = "C-C-C-Combo Breaker! Output didn't match."
            break
        if anyRegex(out, options['regex']):
            combobreaker = "C-C-C-Combo Breaker! Output matched regex."
            break
        if not allRegex(out, options['noregex']):
            combobreaker = "C-C-C-Combo Breaker! Output didn't match regex."
            break
        
    if combobreaker:
        verbose("\n"+combobreaker)
        verbose(" ".join(cmd))
    elif options['zero'] or options['notzero'] or options['match'] or options['nomatch']:
        verbose("\nAll done, no combo breaker")
