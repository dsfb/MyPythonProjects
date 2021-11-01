import pickle


arq = open('arquivo.pkl', 'rb')
x = pickle.load(arq)
arq.close()
print('O arquivo foi lido.')
print(x)
