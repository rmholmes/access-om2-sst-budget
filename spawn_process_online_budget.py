# /usr/bin/env python3

import numpy as np
import os
import fileinput
import time as time_sleeper

outputs = np.arange(336,371) # 336 = 1989, 365=2018
sleep_time = 0
dry = False

# Submit a job for each year:
os.chdir('tmp_qsub_scripts/')
for output in outputs:
    arguments = {'XXOUTPUTXX':str(output),
                    }

    #fscr = 'process_online_budget_year_' + str(output) + '.sub'
    #os.system('cp ../process_online_budget_year.sub ' + fscr)
    fscr = 'process_online_budget_salinity_year_' + str(output) + '.sub'
    os.system('cp ../process_online_budget_year_salinity.sub ' + fscr)
    #os.system('cp ../process_online_hatavg_budget_year.sub ' + fscr)
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