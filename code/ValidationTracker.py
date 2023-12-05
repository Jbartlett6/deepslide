import matplotlib.pyplot as plt 

class ValidationTracker():
    def __init__(self, writer):
        self.scores = {}
        self.total = {}
        self.writer = writer

    def log(self, predictions, labels, filenames):
        
        subjects = [fn.split('/')[-1].split('_')[0]for fn in filenames]
        results = predictions == labels
        for subject, r in zip(subjects, results):
            if r:
                if subject in self.scores:
                    self.scores[subject] += 1
                else:
                    self.scores[subject] = 1

            if subject in self.total:
                self.total[subject] += 1
            else:
                self.total[subject] = 1
                

    def reset(self):
        self.scores = {}
        self.total = {}
        
    def plot_and_save(self, epoch):
        accuracies = [score/total for score, total in zip(self.scores.values(),self.total.values())]
        fig, ax = plt.subplots(1,1)
        ax.bar(self.scores.keys(), accuracies)
        self.writer.add_figure('val/subject_error', fig, global_step = epoch)

