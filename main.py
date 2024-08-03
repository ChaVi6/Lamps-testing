from scipy.stats import mode

import file
import numpy as np
import scipy as scipy
from matplotlib import pyplot

n = file.N  # 146
exp = file.Nexp # 10000
m = file.m  # [18, 27, 28, ..., 32, 36, 33]
s = file.s  # [0, 2, 1, ..., 1, 2, 1]
r = n + 1 # количесвто гипотез

# 1a, 1b
hypotheses = np.arange(r) # массив со всевозможными гипотезами
prior = np.ones(r) / (r) # массив из приорных вероятностей для каждой гипотезы
distribution_range = np.zeros((exp, r)) # массив хранения апостериорных вероятностей гипотез
experiments = np.arange(exp)
experiments += 1 # массив с номерами экспериментов (для графиков)
most_probable_hypothesis = np.zeros((exp, 5)) # массив для записи самых частых гипотез
max_hyp = [7, 8, 6, 9, 5]

for i in range(exp):
    mi = m[i]
    si = s[i]
    likelihood = np.zeros(r) # функция правдоподобия
    for j in range(r):
        likelihood[j] = scipy.stats.binom.pmf(si, mi, j / r)
    posterior = prior * likelihood
    posterior /= np.sum(posterior)
    distribution_range[i] = posterior
    prior = posterior # последняя вычисленная апостериорная вероятность становится новой априорной вероятностью для следующей итерации
    sorted_indices = np.argsort(posterior)[::-1] # получаем индексы элементов в отсортированном порядке
    top_5_indices = sorted_indices[:5] # выбираем первые три индекса
    most_probable_hypothesis[i] = top_5_indices

pyplot.title('Distribution range of posterior probabilities')
pyplot.xlabel('Experiment')
pyplot.ylabel('Probability')
for i in range(r):
    if i in max_hyp:
        label = 'Hypothesis {}'.format(i)
    else:
        label = None
    pyplot.plot(experiments, distribution_range[:, i], label=label)
pyplot.legend()
pyplot.show()


pyplot.title('Top 5 hypotheses')
pyplot.xlabel('Experiment')
pyplot.ylabel('Hypothesis')
for i in range(5):
    pyplot.plot(experiments, most_probable_hypothesis[:, i])
    pyplot.legend(['Top 1', 'Top 2', 'Top 3', 'Top 4', 'Top 5'])
pyplot.show()
print('top1:', mode(most_probable_hypothesis[:, 0])[0])
print('top2:', mode(most_probable_hypothesis[:, 1])[0])
print('top3:', mode(most_probable_hypothesis[:, 2])[0])
print('top4:', mode(most_probable_hypothesis[:, 3])[0])
print('top5:', mode(most_probable_hypothesis[:, 4])[0])

# 1c
limit = 0.01 # отсечка
preval_hypotheses = np.zeros(exp) # массив с числом превалирующих гипотез каждого эксперимента
for i in range(exp):
    for j in range(r):
        if distribution_range[i][j] > limit:
            preval_hypotheses[i] += 1

pyplot.title('Prevailing hypotheses. Limit = 0.01')
pyplot.xlabel('Experiment')
pyplot.ylabel('Number of prevailing hypotheses')
pyplot.plot(experiments, preval_hypotheses)
pyplot.show()

# total
for i in range(r):
    if distribution_range[exp-1][i] == 1:
        print('The most probable number of faulty light bulbs:', i)