# /usr/bin/env python3

import numpy as np
import os
import fileinput
import time as time_sleeper

outputs = [366]
months = [3]#np.arange(1,13)
sleep_time = 0
dry = False

# Submit a job for each year:
os.chdir('tmp_qsub_scripts/')
for output in outputs:
    for month in months:
        arguments = {'XXOUTPUTXX':str(output),
                     'XXMONTHXX':str(month),
                        }
    
        fscr = 'process_offline_daily_budget_output_' + str(output) + '_month_' + str(month) + '.sub'
        os.system('cp ../process_offline_daily_budget_month.sub ' + fscr)
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