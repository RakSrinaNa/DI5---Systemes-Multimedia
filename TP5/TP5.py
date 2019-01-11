import numpy as np
from math import sqrt
from math import floor

def read_data(file, nbuser, nbfilm):
	res = np.ones((nbuser, nbfilm))
	res = res * -1
	fichier = open(file, "rU")
	list_noeuds = fichier.readlines()
	for line in list_noeuds:
		line_split = line.split("\t")
		res[int(line_split[0]) -1][int(line_split[1]) -1] = int(line_split[2])
	return res

def calcmoyuser(line):
	tot = 0.0
	count = 0
	for i in line:
		if i >= 0:
			count += 1		
			tot += i
	return tot/count

def calcmoyfilm(data, i):
	tot = 0.0
	count = 0
	for j in data:
		if j[i] >= 0:
			count += 1		
			tot += j[i]
	return tot/count

def calcmoy(data):
	count = 0
	sum = 0.0
	for l in data:
		for i in l:
			if i >=0:
				count += 1
				sum += i
	return sum / count


def RMSE_alea(alea, data):
	sum = 0.0
	count = 0
	for j in data:
		for i in j:
			if i >= 0:
				sum += (alea - i)**2
				count += 1
	return sqrt(sum/count)

def RMSE_pred(pred, data):
	sum = 0.0
	count = 1
	for j in range(0, len(data)):
		for i in range(0, len(data[j])):
			if data[j][i] >= 0:
				sum += (pred[j][i] - data[j][i])**2
				count += 1
	return sqrt(sum/count)

def calcscore(data, pred, i, j):
	dessus = 0
	for u in range(0, len(pred)):
		dessus += pred[u][i] * pred[u][j]
	dessous1 = 0
	for u in range(0, len(data)):
		if data[u][i] >= 0:
			dessous1 += data[u][i]**2
	dessous2 = 0
	for u in range(0, len(data)):
		if data[u][j] >= 0:
			dessous2 += data[u][j]**2
	
	return dessus / (sqrt(dessous1 * dessous2))

def clacg(rbar, moyuser, moyfilm, score_s, pred_n, u, i, L):
	scores = []
	for w in range(0, len(score_s)):
		if w != i:
			scores.append((w, scores_s[i][w]))
	scores_sorted = sorted(enumerate(scores), key=lambda x: x[1])
	scores_sorted.reverse()	
	li = scores_sorted[:L]

	dessus = 0
	for w in li:
		dessus += score_s[i][w] * pred_n[u][w]
	dessous = 0
	for w in li:
		dessous += abs(score_s[i][w])	

	return rbar + moyuser[u] + moyfilm[i] + (dessus / dessous)


data = read_data("./ml-100k/u.data", 943, 1682)

moyuser = []
for i in range(0, 943):
	moyuser.append(calcmoyuser(data[i]))
moyfilm = []
for i in range(0, 1682):
	moyfilm.append(calcmoyfilm(data, i))

pred_alea = floor(np.random.random() *5+1)
print("Prediction Alea={alea}".format(alea=pred_alea))
rmse_alea = RMSE_alea(pred_alea, data)
print("RMSE Alea={rmse}".format(rmse=rmse_alea))

rbar = calcmoy(data)
pred_basic = np.ones((943, 1682))
pred_basic = pred_basic * -1

for l in range(0, len(pred_basic)):
	for i in range(0, len(data[l])):
		if data[l][i] >= 0:
			pred_basic[l][i] = rbar + (moyuser[l]-rbar) + (moyfilm[i]-rbar)
rmse_pred_basic = RMSE_pred(pred_basic, data)
print("RMSE Basic={rmse}".format(rmse=rmse_pred_basic))

pred_n = np.ones((943, 1682))
pred_n = pred_n * -1

for l in range(0, len(pred_n)):
	for i in range(0, len(data[l])):
		if data[l][i] >= 0:
			pred_n[l][i] = data[l][i] - (rbar + moyuser[l] + moyfilm[i])

rmse_pred_n = RMSE_pred(pred_n, data)
print("RMSE Neighbor={rmse}".format(rmse=rmse_pred_n))

score_s = np.ones((1682, 1682))
score_s = score_s * -1

for l in range(0, len(score_s)):
	for i in range(0, len(pred_n[l])):
		score_s[l][i] = calcscore(data, pred_n, l, i)

pred_g = np.ones((943, 1682))
pred_g = pred_g * -1
for l in range(0, len(pred_g)):
	for i in range(0, len(data[l])):
		if data[l][i] >= 0:
			pred_g[l][i] = clacg(rbar, moyuser, moyfilm, score_s, pred_n, l, i, 20)

rmse_pred_g = RMSE_pred(pred_g, data)
print("RMSE Good={rmse}".format(rmse=rmse_pred_g))

