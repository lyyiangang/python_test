import re
import collections

perf_log_path = '/home/lyy/tmp/dms_new/perf_new.log'
name_to_time =collections.OrderedDict()
name_to_cnt = {}
with open(perf_log_path, 'r') as fid:
    for line in fid:
        match = re.match('^(.*) consumes:(.*) ms', line)
        if match is not None:
            name = match.groups()[0]
            time = float(match.groups()[1])
            if name not in name_to_time.keys():
                name_to_time[name] = time
                name_to_cnt[name] = 1
            else:
                name_to_time[name] += time
                name_to_cnt[name] += 1

for k, v in name_to_time.items():
    print(f'avg time {k} {v/name_to_cnt[k]}')
