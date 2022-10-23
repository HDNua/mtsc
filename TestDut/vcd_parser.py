import sys
import os
import re

from StringBuffer import StringBuffer

import pandas as pd
import numpy as np
import pprint



#
in_filename = sys.argv[1]
svseed = sys.argv[2]

#
fin = open(in_filename, 'r')
in_lines = [_line.rstrip('\r\n') for _line in fin.readlines()]
fin.close()

#
sb = StringBuffer(lines=in_lines)

#
pat_scope = re.compile('''^
    \$scope
    \s+
    (?P<TYPE>\w+)
    \s+
    (?P<NAME>\w+)
    \s+
    \$end
    $''', re.VERBOSE)
pat_upscope = re.compile('''^
    \$upscope
    \s+
    \$end
    $''', re.VERBOSE)
pat_var = re.compile('''^
    \$var
    \s+
    (?P<TYPE>\w+)
    \s+
    (?P<WIDTH>\d+)
    \s+
    (?P<ID>[^\s]+)
    \s+
    (?P<NAME>\w+)
    \s*
    (?P<RANGE>\[
        (?P<MSB>\d+)
        \:
        (?P<LSB>\d+)
        \]
    )?
    \s+
    \$end
    $''', re.VERBOSE)
pat_end = re.compile('^\$end')

pat_time = re.compile('''^
    \#(?P<TIME>\d+)
    $''', re.VERBOSE)
pat_vc = re.compile('''^
    (?P<VALUE>\w+)\s*(?P<ID>[^\s]+)
    $''', re.VERBOSE)
pat_dumpall = re.compile('''^
    \$dumpall
    $''', re.VERBOSE)


#
v_dict = {}


#
scope_stack_array = []
scope_stack_index = 0


#
vid_list = []
var_list = []


#
def parse_var(sb: StringBuffer, match: re.Match):
    global v_dict, vid_list, var_list
    g_type = match.group('TYPE')
    g_width = int(match.group('WIDTH'))
    g_id = match.group('ID')
    g_name = match.group('NAME')
    g_range = match.group('RANGE')
    g_range_msb = match.group('MSB')
    g_range_lsb = match.group('LSB')

    #
    path = '.'.join(scope_stack_array)

    #
    v_hier = '.'.join(scope_stack_array)
    if g_width > 1:
        print('%s; %s %s%s == %s' %(path, g_type, g_name, g_range, g_id))

        #
        v_name = f'{v_hier}.{g_name}{g_range}'
        v_dict[g_id] = v_name

        #
        vid_list.append(g_id)
        var_list.append(v_name)

    else:
        print('%s; %s %s == %s' %(path, g_type, g_name, g_id))

        #
        v_name = f'{v_hier}.{g_name}'
        v_dict[g_id] = v_name

        #
        vid_list.append(g_id)
        var_list.append(v_name)
    

#
def parse_scope(sb: StringBuffer, match: re.Match):
    global scope_stack_array, scope_stack_index

    g_type = match.group('TYPE')
    g_name = match.group('NAME')
    scope_stack_array.append(g_name)
    scope_stack_index += 1

    while sb.reading():
        line = sb.getline()

        #
        m = pat_upscope.search(line)
        if m is not None:
            scope_stack_array.pop()
            return

        #
        m = pat_scope.search(line)
        if m is not None:
            parse_scope(sb=sb, match=m)
            continue

        #
        m = pat_var.search(line)
        if m is not None:
            parse_var(sb=sb, match=m)
            continue


#
time_list = []


##
#df = pd.DataFrame({"vid": vid_list, "var": var_list})
#df.set_index("vid")

#
#pprint.pprint(df)

#
time = 0
df = None
while sb.reading():
    line = sb.getline()

    #
    m = pat_scope.search(line)
    if m is not None:
        parse_scope(sb=sb, match=m)
        continue

    #
    m = pat_time.search(line)
    if m is not None:
        #print('pat_time: line = [%s]' %(line))
        time = int(m.group('TIME'))
        time_list.append(time)

        #
        len_var_list = len(var_list)
        new_df = pd.DataFrame({time: np.nan}, columns=[time])
        df = pd.concat((df, new_df), axis=1)
        continue

    #
    m = pat_vc.search(line)
    if m is not None:
        s_value = m.group('VALUE')
        id = m.group('ID')

        #
        v_lvalue = v_dict[id]

        #
        ret = df[time]
        #pprint.pprint(ret)

        #
        value = s_value
        #if s_value == 'x':
        #    value = np.nan
        #elif s_value.startswith('b'):
        #    value = int(s_value[1:], 2)
        #elif s_value.startswith('h'):
        #    value = int(s_value[1:], 16)
        #else:
        #    value = int(s_value)


        #
        df[time][id] = value

        #
        #print('(%s, %s, %s)' %(v_lvalue, time, value))
        continue

    #
    m = pat_dumpall.search(line)
    if m is not None:
        df = pd.DataFrame({"vid": vid_list, "var": var_list})
        df.index = vid_list
        continue


df = df.fillna(method='ffill', axis=1)
#pprint.pprint(df)

csv_filename = f'csv/dump.{svseed}.csv'
df.to_csv(csv_filename, index=False)