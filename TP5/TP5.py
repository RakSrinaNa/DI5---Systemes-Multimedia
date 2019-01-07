import numpy as np

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


def RMSE_alea(alea, line):
	sum = 0.0
	count = 0
	for i in line:
		if i >= 0:
			sum += (alea - i)**2
			count += 1
	return sum / count

def RMSE_pred(pred, line):
	sum = 0.0
	count = 0
	for i in range(0, len(line)):
		if line[i] >= 0:
			sum += (pred[i] - line[i])**2
			count += 1
	return sum / count

data = read_data("./ml-100k/u.data", 943, 1682)

moyuser = []
for i in range(0, 943):
	moyuser.append(calcmoyuser(data[i]))
moyfilm = []
for i in range(0, 1682):
	moyfilm.append(calcmoyfilm(data, i))


rmse_alea = []
alea = np.random.random() *5
for i in range(0, 943):
	rmse_alea.append(RMSE_alea(alea, data[i]))


rbar = calcmoy(data)
pred_basic = np.ones((943, 1682))
pred_basic = pred_basic * -1

for l in range(0, len(pred_basic)):
	for i in range(0, len(data[l])):
		if data[l][i] >= 0:
			pred_basic[l][i] = rbar + (moyuser[l]-rbar) + (moyfilm[i]-rbar)
rmse_pred_basic = []
for i in range(0, 943):
	rmse_pred_basic.append(RMSE_pred(pred_basic[i], data[i]))
print(rmse_pred_basic)
