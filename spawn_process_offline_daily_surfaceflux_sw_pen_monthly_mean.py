# /usr/bin/env python3

import os
import fileinput
import time as time_sleeper

outputs = [366]
sleep_time = 0
dry = False

# Submit a job for each year:
os.chdir('tmp_qsub_scripts/')
for output in outputs:
    arguments = {'XXOUTPUTXX':str(output),
                    }

    fscr = 'process_offline_daily_surfaceflux_sw_pen_monthly_mean_output_' + str(output) + '.sub'
    os.system('cp ../process_offline_daily_surfaceflux_sw_pen_monthly_mean.sub ' + fscr)
    with fileinput.FileInput(fscr, inplace=True) as file:
        for line in file:
            line_out = line
            for arg in arguments.keys():
                line_out = line_out.replace(arg,arguments[arg])
            print(line_out, end='')
    if not dry:
        os.system('qsub ' + fscr)
    if not dry:
        print('Waiting %02ds after output %04d' % (sleep_time,output))
        time_sleeper.sleep(sleep_time)
