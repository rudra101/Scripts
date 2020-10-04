#create new datasets A' and B' out of two datasets A and B such that (meanA', stdA') is not significantly different from (meanB', stdB').
import numpy as np
from scipy import stats
import random

##example asd and control data below. List of tuples - (age, FIQ)
#filter_asd_males = [(21.6482, 117), (20.1697, 108), (20.1807, 92), (20.178, 91), (22.8802, 113), (29.0897, 127), (27.4114, 94), (21.4346, 96), (19.7043, 102), (23.5948, 132), (25.7972, 86), (25.4511, 100), (19.6277, 110), (26.9487, 125), (32.5503, 126), (37.7769, 65), (24.3231, 129), (34.4613, 80), (21.1307, 99), (25.4346, 113), (32.9582, 90), (28.6708, 80), (33.1828, 95), (28.1095, 97), (26.3792, 107), (21.4018, 109), (18.4175, 80), (32.8487, 106), (18.4148, 93), (28.0903, 112)];

#filter_control_males = [(18.2806, 131), (18.2615, 93), (22.601, 128), (23.948, 98), (27.5975, 123), (26.8528, 127), (24.9884, 100), (18.1383, 128), (27.3238, 116), (18.2177, 108), (21.0979, 95), (29.9685, 112), (18.8008, 111), (31.2827, 112), (34.0534, 123), (26.1465, 148), (18.1547, 111), (24.6543, 120), (28.3669, 121), (34.0068, 129), (39.2526, 103), (19.7591, 89), (39.3949, 122), (28.5613, 134), (25.0157, 108), (22.1081, 104), (22.4367, 106), (22.0479, 110)];

def ageFIQMatcher(asd_data, control_data, ITER_CNT=10**5):
    N_asd = len(asd_data)
    N_control = len(control_data)
    minLen = min(N_asd, N_control)
    print('Got %d asd, %d control' %(N_asd, N_control))
    #ITER_CNT = 10**5 
    [MIN_t_fiq, MIN_t_age, MAX_p_age, MAX_p_fiq] = [10**4,10**4,0,0]
    desired_asd_sample = []; desired_control_sample = [];
    for n_asd in range(minLen, min(10,minLen), -1):
        min_num = max(min(10,minLen), n_asd-3); max_num = min(N_control,n_asd+3);
        for n_control in range(min_num, max_num):
            print('Running sim for n_asd = %d, n_control = %d'% (n_asd, n_control))
            cnt = ITER_CNT
            [max_p_age, max_p_fiq] = [0,0]
            curr_asd_sample = []; curr_control_sample = [];
            [min_t_age,min_t_fiq] = [10**4,10**4];
            matched = set()
            while cnt > 0:
                matched.clear()
                cnt = cnt - 1
                sample_asd = random.sample(asd_data, n_asd)
                sample_control = random.sample(control_data, n_control)
                if not len(sample_asd) or not len(sample_control):
                    continue
                sample_asd_age = [val[1] for val in sample_asd]
                sample_asd_fiq = [val[2] for val in sample_asd]
                sample_control_age = [val[1] for val in sample_control]
                sample_control_fiq = [val[2] for val in sample_control]
                t_age, p_age = stats.ttest_ind(sample_asd_age, sample_control_age)
                t_fiq, p_fiq = stats.ttest_ind(sample_asd_fiq, sample_control_fiq)
                if (abs(t_age) > 0.2) or (abs(t_fiq)> 1.2) or min(min(sample_asd_fiq),min(sample_control_fiq)) < 89:
                    continue
                elif (abs(t_age) <= 0.2):
                    if min_t_fiq > abs(t_fiq) and max_p_fiq <= p_fiq:
                        min_t_fiq = abs(t_fiq)
                        max_p_fiq = p_fiq
                        curr_asd_sample = sample_asd
                        curr_control_sample = sample_control
                #if min_t_age > abs(t_age) and max_p_age <= p_age:
                #    min_t_age = abs(t_age)
                #    max_p_age = p_age
                #    max_p_fiq = p_fiq
                #    min_t_fiq = abs(t_fiq)
                #    curr_asd_sample = sample_asd
                #    curr_control_sample = sample_control
                #elif (min_t_age == abs(t_age) and max_p_age == p_age):
                #    if min_t_fiq > abs(t_fiq) and max_p_fiq <= p_fiq:
                #        min_t_fiq = abs(t_fiq)
                #        max_p_fiq = p_fiq
                #        curr_asd_sample = sample_asd
                #        curr_control_sample = sample_control 
            if MIN_t_fiq > min_t_fiq and MAX_p_fiq <= p_fiq:
                MIN_t_fiq = min_t_fiq
                MAX_p_fiq = p_fiq
                desired_asd_sample = curr_asd_sample
                desired_control_sample = curr_control_sample 
            
            #if MIN_t_age > min_t_age and MAX_p_age <= max_p_age:
            #    MIN_t_age = min_t_age
            #    MAX_p_age = max_p_age
            #    MAX_p_fiq = max_p_fiq
            #    MIN_t_fiq = min_t_fiq
            #    desired_asd_sample = curr_asd_sample
            #    desired_control_sample = curr_control_sample
            #elif (MIN_t_age == min_t_age) and (MAX_p_age == max_p_age):
            #    if MIN_t_fiq > min_t_fiq and MAX_p_fiq <= p_fiq:
            #        MIN_t_fiq = min_t_fiq
            #        MAX_p_fiq = p_fiq
            #        desired_asd_sample = curr_asd_sample
            #        desired_control_sample = curr_control_sample
            #print('As of now. t_age=%f, p_age=%f, t_fiq=%f, p_fiq=%f' %(MIN_t_age,MAX_p_age,MIN_t_fiq,MAX_p_fiq))
            #if (MIN_t > min_t) or (min_t == MIN_t and sample_p_fiq > FINAL_p_fiq):
            #    #(MAX_p_age < max_p_age) or (MAX_p_age == max_p_age and sample_p_fiq > FINAL_p_fiq): 
            #    MIN_t_diff = min_t
            #    #MAX_p_age = max_p_age
            #    FINAL_p_fiq = sample_p_fiq
            #    desired_asd_sample = curr_asd_sample
            #    desired_control_sample = curr_control_sample

    print('desired sample')

    sample_asd_age = [val[1] for val in desired_asd_sample]
    sample_asd_fiq = [val[2] for val in desired_asd_sample]
    sample_control_age = [val[1] for val in desired_control_sample]
    sample_control_fiq = [val[2] for val in desired_control_sample]
    if len(desired_asd_sample) and len(desired_control_sample):
        print('asd(N=%d). mean(age) = %f±%f,mean(fiq) = %f±%f ' %(len(sample_asd_age), np.mean(sample_asd_age), np.std(sample_asd_age),np.mean(sample_asd_fiq), np.std(sample_asd_fiq)))
        print('control(N=%d). mean(age) = %f±%f,mean(fiq) = %f±%f' %(len(sample_control_age), np.mean(sample_control_age), np.std(sample_control_age),np.mean(sample_control_fiq), np.std(sample_control_fiq)))
        t_age,p_age=stats.ttest_ind(sample_asd_age,sample_control_age)
        t_fiq,p_fiq=stats.ttest_ind(sample_asd_fiq,sample_control_fiq)
        print('t_age=%f,p_age=%f, asd_range(age)=(%f,%f), cntr_range(age)=(%f,%f)'%(t_age,p_age, min(sample_asd_age), max(sample_asd_age), min(sample_control_age), max(sample_control_age)))
        print('t_fiq=%f,p_fiq=%f, asd_range(fiq)=(%f,%f), cntr_range(fiq)=(%f,%f)'%(t_fiq,p_fiq, min(sample_asd_fiq), max(sample_asd_fiq), min(sample_control_fiq), max(sample_control_fiq)))
    else:
        print('No matching data found')
    #print('asd data=', curr_asd_sample)
    #print('cntrl data=', curr_control_sample)
    return desired_asd_sample, desired_control_sample

