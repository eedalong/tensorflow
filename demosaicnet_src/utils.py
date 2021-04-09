import torch
import matplotlib.pyplot as plt
import os
def save_checkpoint(model,path_checkpoint):

    torch.save(model.state_dict(),path_checkpoint);

class AverageMeter:
    def __init__(self):
        self.n = 0;
        self.value = 0;
    def update(self,value,count = 1):
        if float(value) == float('inf'):
            return ;
        self.value = (self.value * self.n + value * count) / (self.n + count);
        self.n = self.n + count;
        return ;


class Recorder:
    def __init__(self,save_freq = 1,save_dir = './'):
        self.records = {};
        self.freq = save_freq;
        self.save_dir = save_dir;
    def add_record(self,record_name,value,steps):
        if self.records.get(record_name,'dalong') == 'dalong':
           self.records[record_name] = {};
        self.records[record_name][steps] = value;
        if steps % self.freq == 0:
            pass
            #self.DrawGraph(record_name);
    def DrawGraph(self,record_name):
        figure = plt.figure(record_name);
        plt.plot(self.records[record_name].keys(),self.records[record_name].values());
        figure.savefig(os.path.join(self.save_dir,record_name+'.png'));

def save_logs(root_path,args):
    log_file = open(os.path.join(root_path,'log_file'),'w');
    log = vars(args);
    for key in log :
        log_file.write(key + ' : ' + str(log[key]) + '\n');
    log_file.close();


def main():
	print('This is for saving models');

if __name__ == '__main__':
	main();

