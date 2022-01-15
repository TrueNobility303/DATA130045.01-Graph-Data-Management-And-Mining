import subprocess
import os
import sys
import time
from tqdm import tqdm

file_dir = '/home/yanglei/GraphEditDistance/Syn/'
   
def command(cmd, timeout=60): 
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True) 
    t_beginning = time.time() 
    seconds_passed = 0 
    while True: 
        if p.poll() is not None: 
            break 
        seconds_passed = time.time() - t_beginning 
        if timeout and seconds_passed > timeout: 
            p.terminate() 
            return "-1\n".encode()
        time.sleep(1) 
    return p.stdout.read() 

def cal_ged(start,end,task,file_dir,timeout=60):
    result = ""
    for i in range(start, end):
        file1 = task[i][0]
        file2 = task[i][1]
        cmd_tmp = 'python src/ged.py '+file_dir+'test/'+file1+' '+file_dir+'test/'+file2+' BM 10 0'
        result = result + file1 + '\t' + file2 + '\t' + command(cmd_tmp,timeout).decode()
    return result

def load_task(file_dir):
    file_dir_train = file_dir+'train/'
    files_train = os.listdir(file_dir_train)
    file_dir_test = file_dir+'test/'
    files_test = os.listdir(file_dir_test)
    task = []
    for file1 in files_train:
        for file2 in files_test:
            if file1.split('.')[1] == 'gexf' and file2.split('.')[1] == 'gexf' and file1 != file2:
            # if file1.split('.')[1] == 'gxl' and file2.split('.')[1] == 'gxl':              
                task.append([file1,file2])
    print (len(task))
    return task

def load_task_trip(file_dir):
    file_dir_train = file_dir+'test/'
    files_train = os.listdir(file_dir_train)
    task = []
    for i in range(int(len(files_train)/3)):
        file1 = str(i)+'_1.gexf'
        file2 = str(i)+'_2.gexf'
        file3 = str(i)+'_3.gexf'
        if file1 in files_train and file2 in files_train and file3 in files_train:
            task.append([file1,file2])
            task.append([file1,file3])
    print (len(task))
    return task


def main():
    jobs = []
    # task = load_task(file_dir)
    task = load_task_trip(file_dir)
    start = 0
    timeout = 360
    end = len(task)
    if len(sys.argv) > 1:
        ncpus = int(sys.argv[1])
    else:
        ncpus = 20
    step = end / ncpus
    for i in range(0, ncpus):
        ss = int(i * step)
        ee = int(ss + step)
        if ee > end:
            ee == end
        jobs.append((cal_ged, (ss, ee, task, file_dir, timeout),(command,), modules=('subprocess','time',)))
    results = ""
    for job in jobs:
        result = str(job())
        results += result

    with open(file_dir+'ged.txt','w') as fout:
        fout.write(results)
    fout.close()
    print ("Successfully preprocess!")

if __name__ == "__main__":
    main()  
