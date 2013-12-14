import web
import string
import random
import copy
import json

urls=('/','Index',
	'/history','Json')
render=web.template.render('templates/')

class Json:
	def GET(self):
		f=open("index.json","r")
		s=f.read()
		f.close()
		return s

class Index:
	def execute(self,f,n,m,h,v):
		his = []
		que = [[-1,0]]
		maxv = {'sum':f[0][0],'a':0,'b':0,'c':0,'d':0}
		if h or v:
			for i in range(0,n):
				if h:
					f[i] += f[i]
				if v:
					f += [f[i]]
		M = m
		if h:
			M = 2*m
		N = n
		if v:
			N = 2*n
		for i in range(0,n):
			p = [0]*M
			for j in range(i,min(N,i+n)):
				sumv = 0
				que = [[-1,0]]
				for k in range(0,M):
					while len(que)>=1 and k-que[0][0]>m:
						que.pop(0)
					p[k] += f[j][k]
					sumv += p[k]
					nowv = {}
					nowv['sum'] = sumv-que[0][1] 
					nowv['a'] = i % n 
					nowv['b'] = (que[0][0]+1)%m
					nowv['c'] = j % n
					nowv['d'] = k % m
					if nowv['sum']> maxv['sum']:
						maxv = copy.deepcopy(nowv)				
					his.append({'max':maxv,'now':nowv})	
					while len(que)>=1 and que[len(que)-1][1]>sumv:
						que.pop(len(que)-1)
					que.append([k,sumv])	
		f = open("index.json","w")
		json.dump(his,f)	
		f.close()

	def GET(self):
		return render.index(0,0,[[0]],5,5)

	def POST(self):
		x=web.input(myfile={})
		if x['myfile'].value!='':
			f = x['myfile'].value
			f = f.split("\n")
			n = string.atoi(f[0].replace(",",""))
			m = string.atoi(f[1].replace(",",""))
			f = f[2:]
			f = [[string.atoi(j) for j in i.split(",")] for i in f if i is not '']
		else:
			n=string.atoi(x['hsize'])
			m=string.atoi(x['lsize'])
			f=[]
			for i in range(0,n):
				f += [[]]
				for j in range(0,m):
					f[i].append(random.randint(-100,100))	
		self.execute(f,n,m,"h" in x,"v" in x)
		return render.index(n,m,f,n,m)

if __name__ == "__main__":
	app=web.application(urls,globals())
	app.run()
