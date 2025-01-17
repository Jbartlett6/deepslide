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
        subs = self.scores.keys()
        accuracies = [self.scores[sub]/self.total[sub] for sub in subs]
        ordered_scores = [self.scores[sub] for sub in subs]
        ordered_totals = [self.total[sub] for sub in subs]
        
        fig, ax = plt.subplots(1,3)

        ax[0].bar(self.scores.keys(), accuracies)
        ax[1].bar(self.scores.keys(), ordered_scores)
        ax[2].bar(self.scores.keys(), ordered_totals)

        self.writer.add_figure('Val/Subject Accuracies', fig, global_step = epoch)


