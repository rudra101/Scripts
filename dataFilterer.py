#create new datasets A' and B' out of two datasets A and B such that (meanA', stdA') is not significantly different from (meanB', stdB').
import numpy as np
from scipy import stats
import random

filter_asd_males = [(21.6482, 117), (20.1697, 108), (20.1807, 92), (20.178, 91), (22.8802, 113), (29.0897, 127), (27.4114, 94), (21.4346, 96), (19.7043, 102), (23.5948, 132), (25.7972, 86), (25.4511, 100), (19.6277, 110), (26.9487, 125), (32.5503, 126), (37.7769, 65), (24.3231, 129), (34.4613, 80), (21.1307, 99), (25.4346, 113), (32.9582, 90), (28.6708, 80), (33.1828, 95), (28.1095, 97), (26.3792, 107), (21.4018, 109), (18.4175, 80), (32.8487, 106), (18.4148, 93), (28.0903, 112)];

filter_control_males = [(18.2806, 131), (18.2615, 93), (22.601, 128), (23.948, 98), (27.5975, 123), (26.8528, 127), (24.9884, 100), (18.1383, 128), (27.3238, 116), (18.2177, 108), (21.0979, 95), (29.9685, 112), (18.8008, 111), (31.2827, 112), (34.0534, 123), (26.1465, 148), (18.1547, 111), (24.6543, 120), (28.3669, 121), (34.0068, 129), (39.2526, 103), (19.7591, 89), (39.3949, 122), (28.5613, 134), (25.0157, 108), (22.1081, 104), (22.4367, 106), (22.0479, 110)];

N_asd = len(filter_asd_males)
N_control = len(filter_control_males)
ITER_CNT = 6*10**4 
[MIN_t_diff, MAX_p_age, Final_p_fiq] = [1000,0,0]
desired_asd_sample = []; desired_control_sample = [];
for n_asd in range(N_asd, 11, -1):
    min_num = max(12, n_asd-5); max_num = min(N_control, n_asd+5);
    for n_control in range(min_num, max_num+1, 1):
        print('Running sim for n_asd = %d, n_control = %d'% (n_asd, n_control))
        cnt = ITER_CNT
        [max_p_age, sample_p_fiq] = [0,0]
        curr_asd_sample = []; curr_control_sample = [];
        min_t_diff = 10000;
        matched = set()
        while cnt > 0:
            matched.clear()
            cnt = cnt - 1
            sample_asd = random.sample(filter_asd_males, n_asd)
            sample_control = random.sample(filter_control_males, n_control)
            sample_asd_age = [val[0] for val in sample_asd]
            sample_asd_fiq = [val[1] for val in sample_asd]
            sample_control_age = [val[0] for val in sample_control]
            sample_control_fiq = [val[1] for val in sample_control]
            age_match = True
            for index_asd in range(0,len(sample_asd_age)):
                found = False
                for index_control in range(0,len(sample_control_age)):
                    if index_control not in matched and abs(sample_asd_age[index_asd]-sample_control_age[index_control])<=0.6:
                        matched.add(index_control)
                        found = True
                        break
                if not found:
                    age_match = False
                    break
            if not age_match:
                continue
            #t_age, p_age = stats.ttest_ind(sample_asd_age, sample_control_age)
            t_fiq, p_fiq = stats.ttest_ind(sample_asd_fiq, sample_control_fiq)
            if (min_t_diff > abs(1-t_fiq)) or (min_t_diff == abs(1-t_fiq) and p_fiq > sample_p_fiq) :
                min_t_diff = abs(1-t_fiq)
                #(max_p_age < p_age) or (max_p_age == p_age and p_fiq > sample_p_fiq):
                #max_p_age = p_age
                sample_p_fiq = p_fiq
                curr_asd_sample = sample_asd
                curr_control_sample = sample_control
        if (MIN_t_diff > min_t_diff) or (min_t_diff == MIN_t_diff and sample_p_fiq > FINAL_p_fiq):
            #(MAX_p_age < max_p_age) or (MAX_p_age == max_p_age and sample_p_fiq > FINAL_p_fiq): 
            MIN_t_diff = min_t_diff
            #MAX_p_age = max_p_age
            FINAL_p_fiq = sample_p_fiq
            desired_asd_sample = curr_asd_sample
            desired_control_sample = curr_control_sample

print('desired sample')

sample_asd_age = [val[0] for val in desired_asd_sample]
sample_asd_fiq = [val[1] for val in desired_asd_sample]
sample_control_age = [val[0] for val in desired_control_sample]
sample_control_fiq = [val[1] for val in desired_control_sample]
print('asd(N=%d). mean(age) = %f±%f,mean(fiq) = %f±%f ' %(len(sample_asd_age), np.mean(sample_asd_age), np.std(sample_asd_age),np.mean(sample_asd_fiq), np.std(sample_asd_fiq)))
print('control(N=%d). mean(age) = %f±%f,mean(fiq) = %f±%f' %(len(sample_control_age), np.mean(sample_control_age), np.std(sample_control_age),np.mean(sample_control_fiq), np.std(sample_control_fiq)))

t_age,p_age=stats.ttest_ind(sample_asd_age,sample_control_age)
t_fiq,p_fiq=stats.ttest_ind(sample_asd_fiq,sample_control_fiq)
print('t_age=%f,p_age=%f'%(t_age,p_age))
print('t_fiq=%f,p_fiq=%f'%(t_fiq,p_fiq))

