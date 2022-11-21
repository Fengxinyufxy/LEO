# -*- coding: UTF-8 -*-
import math

import matplotlib.pyplot as plt
import copy
import random
import networkx as nx
import numpy as np
import time

M=6  #卫星轨道数
N=8	 #每个轨道上的卫星数量

class Graph(object):
	def __init__(self, *args, **kwargs):
		self.node_neighbors = {}  #记录node的邻接情况  以字典形式记录全局  每个node以list形式记录自身信息
		self.visited = {}
		self.A = []  # 为现存节点数组  ???
		self.degree = {}  # 为度数组,记录节点的度

	def all_nodes(self):
		keys_list = self.node_neighbors.keys()
		return keys_list

	def add_node(self, node):
		if node not  in self.all_nodes():
			self.node_neighbors[node] = []  #初始化node节点，值为空

	def add_nodes(self, nodes):
		for node in nodes:
			if node not in self.all_nodes():
				self.add_node(node)

	def add_edge(self, u, v):
		if (u != v):
			if u in self.node_neighbors:
				if (v not in self.node_neighbors[u]) and (u not in self.node_neighbors[v]):
					self.node_neighbors[u].append(v)
					self.node_neighbors[v].append(u)
		else:
			print(str(u)+"not exist!")

	def add_edges(self, list):
		for item in list:
			self.add_edge(item[0],item[1])
	"""
	param:
	 	nodes:record neighbor nodes
	 	degree:{},record every node's degree
	"""
	def get_degree(self):
		self.degree.clear()
		nodes=self.all_nodes()
		all_degree={}
		for node in nodes:
			all_degree[node]=len(self.node_neighbors[node])
			#print("节点"+str(node)+"的度为："+str(len(self.node_neighbors[node])))
		self.degree=all_degree
	"""
	param: 
		odd_degree_nodes[]:according to degree{} get the degree and calculate to get odd_degree_nodes[]
	"""
	def odd_nodes(self):
		odd_degree_nodes=[]
		self.get_degree()
		for k,v in self.degree.items():
			if v % 2 != 0:
				odd_degree_nodes.append(k)
		# print("奇点为",odd_degree_nodes)
		return odd_degree_nodes

"""
好像没封装好，还得继续修改，del_edge应该封装进类
"""


def del_edge(graph, u, v):
	if u not in graph.node_neighbors or v not in graph.node_neighbors:
		print("node "+str(u)+" is not exist!")
	if(u!= v):
		if (u in graph.node_neighbors[v]) and (v in graph.node_neighbors[u]):
			graph.node_neighbors[u].remove(v)
			graph.node_neighbors[v].remove(u)


"""
use the networkx to show the topo
"""

# def graph_generator():
def show_graph(graph):
	G = nx.Graph()
	for k,v in graph.node_neighbors.items():
		G.add_node(k)
		for i in v:
			G.add_edge(k,i)
	nx.draw_networkx(G)
	plt.show()


# def get_subgraph(graph):  # 求所有联通子图
# 	seen = set()
# 	subgraph=Graph()
# 	subgraph.node_neighbors=copy.deepcopy(graph.node_neighbors)
# 	for v in graph:
# 		if v not in seen:
# 			c = bfs(G, v)
# 			seen.update(c)
# 			yield c
# 		subgraph.del_edge(u,v)  #将纵向路径从中删除，得到全部为横向路径的子图
#


def deep_copy(graph):
	graph_copy = copy.deepcopy(graph)
	graph_copy.node_neighbors=copy.deepcopy(graph.node_neighbors)
	return graph_copy



"""
m表示轨道数量，n表示每条轨道上的卫星数量
"""


def vertical_path(graph,m, n):
	vpath_list=[]
	for i in range(1,m+1):
		vpath = []
		for j in range(1,n+1):
			u=i*10+j
			if j+1<=n:
				v=u+1
			else:
				v=i*10+(j+1)%n
			del_edge(graph,u,v)
			vpath.append(u)
		vpath.append(v)
		print("纵向路径为：",vpath)
		vpath_list.append(vpath)
	print("纵向路径集合：",vpath_list)
	return vpath_list

"""
use the processed graph without vertical paths to get the lanscape path.
param:
	source:choose one of the odd nodes randomly as the start node of a landscape path
	lpath:use the 'source' as start node and then  implement the dsf algorithm on the 'graph',finally  get the landscape path
"""
def landscape_path(graph):
	lpath_list=[]
	while len(graph.odd_nodes())>0:
		lpath=[]
		print("奇点",graph.odd_nodes())
		source=random.choice(graph.odd_nodes())
		lpath=dfs(graph,source)
		lpath_list.append(lpath)
		print("横向路径为：",lpath)
		print()
		for i in range(len(lpath)-1):						# 接下来进行将graph中的path进行删除
			del_edge(graph,lpath[i],lpath[i+1])				#不删好像也没啥影响
	print("横向路径集合：",lpath_list)
	return lpath_list
"""
将与横向路径相连的纵向路径随机拼接
但为了防止最后会剩余没有被选择拼接的纵向路径
选择从纵向路径的角度考虑随机与横向路径连接
"""
def combination(v_list, l_list):
	result_list=[]
	random.shuffle(v_list)
	print(v_list)
	for v in v_list:     #将纵向路径中的节点提取出来，与横向路径对比是否有重合，有则进行拼接
		result=[]
		print("v:",v)
		added=0		     #添加标志，记录v是否已被添加，已被添加后，将删除该v  本打算直接删除v 在实际处理时会发现这将会影响的v_list中的元素进行循环，因为list长度在变，而for中则默认长度为初始值
		for l in l_list:
			print("l:",l)
			if added==1:
				# added=0
				break
			else:
				for node in v:
					if node in l:
						l.append(v)
						result.append(l)
						#v_list.remove(v)
						added=1
						print(node)
						print(l)
						break
	print(l_list)
	return l_list
"""
均衡路径要求最后所得遍历路径间的长度差别尽可能的小
算法思路：向横向路径中拼接纵向路径，为了实现最终路径间差距小，每次拼接后，重新
对路径长度进行排序，使得每次总是最短路径优先获得拼接的资格，直接全部拼接完毕
缺陷：
	1.当横向路径较少时，会出现多条纵向拼接在同一条上（实际中横向多于纵向）
	2.之前横向路径选择时可能具有随机性，导致每次结果具有随机性
	3.结果可能不是最优结果，因为是否最优与最先进行选择的横向路径有关：假如某条横向路径相连的纵向路径较少（即长度较短，但不可能是最短
	因为最短会最优先进行选择），但选择机会没那么靠前，考虑是否全会被选走？？？但因为纵向必定长于横向，好像一旦拼接后，就会位次就会排到后面。。。。
	暂时好像不用考虑
	
核心：每次拼接都从最短优先进行

进一步优化：
	l_list中apend v后，会扰乱原有的list,虽然便于直接比较，但后续无法进行操作
	修改：l_list重新排序不依据元素多少，而是重新定义排序规则
	
	
param:
	v_record:用来记录v_list的长度，每当v_list减少时就刷新值，并跳出本次循环，当发现v_record不是此时v_list的长度时，说明
	存在匹配不成功或首次进行匹配
"""

def balanced_combination(v_list, l_list):
	l_list.sort(key = lambda i:len(i))
	print("l_list:",l_list)
	v_record=0
	while(len(v_list)>0):
		added=0

		
		# if v_record==len(v_list):
		for l in l_list:
			for node in l:
				if(added==1):break
				print(node)
				for v in v_list:
					print("v",v)
					if node in v:
						print("交点node",node)
						print("l",l)
						l.append(v)
						v_list.remove(v)
						print("v_list",v_list)
						l_list=path_sort(l_list)
						print("重新排序后",l_list)
						added=1
						v_record=len(v_list)
						break
	cal_variance(l_list)
	return l_list
# def balanced_combination(v_list, l_list):
# 	l_list.sort(key = lambda i:len(i))
# 	print("l_list:",l_list)
# 	v_record=0
# 	while(len(v_list)>0):
# 		added=0
# 		# if v_record==len(v_list):
# 		for l in l_list:
# 			for node in l:
# 				if(added==1):break
# 				print(node)
# 				for v in v_list:
# 					print("v",v)
# 					if node in v:
# 						print("交点node",node)
# 						print("l",l)
# 						l.extend(v)
# 						v_list.remove(v)
# 						print("v_list",v_list)
# 						l_list.sort(key = lambda i:len(i))
# 						print("重新排序后",l_list)
# 						added=1
# 						v_record=len(v_list)
# 						break
# 		cal_variance(l_list)
		# else:
		# 	for node in l_list[0]:
		# 		if(added==1):break
		# 		print(node)
		# 		for v in v_list:
		# 			print("v",v)
		# 			if node in v:
		# 				print("node",node)
		# 				print("l_list",l_list[0])
		# 				l_list[0].extend(v)
		# 				v_list.remove(v)
		# 				print("v_list",v_list)
		# 				l_list.sort(key = lambda i:len(i))
		# 				print("重新排序",l_list)
		# 				added=1
		# 				v_record=len(v_list)
		# 				break


def path_sort(paths):
	l=[]
	for path in paths:
		# count=0
		# for nodes in path:
		# 	if isinstance(nodes,list):
		# 		# for node in nodes:
		# 		# 	count=count+1
		# 		count=count+N+1
		# 	else:
		# 		count=count+1
		count=cal_length(path)
		tp=(path,count)
		l.append(tp)
		print(tp)
		print(path)
		print(count)
		print(l)
	m=sorted(l,key=lambda tp:tp[1])
	print(m)
	sorted_path=[]
	for item in m:
		sorted_path.append(item[0])
	print(sorted_path)
	return sorted_path





def get_traverse(path_list):
	for path in path_list:
		subgraph=Graph()
		v_path=[]   #存放纵向路径
		l_path=[]   #存放横向路径
		for node in path:                 #添加子图节点
			if isinstance(node,list):
				print("纵向：",node)
				v_path.append(node)
				for i in node:
					subgraph.add_node(i)
			else:
				l_path.append(node)
				subgraph.add_node(node)
		#print("邻接链表Node",subgraph.node_neighbors)
		print("path",path)
		print("lpath",l_path)
		print("vpath",v_path)
		for v in v_path:
			for i in range(0,len(v)-1):
				subgraph.add_edge(v[i],v[i+1])
		print(subgraph.node_neighbors)
		show_graph(subgraph)
		for i in range(0,len(l_path)-1):
			subgraph.add_edge(l_path[i],l_path[i+1])
		print("邻接链表",subgraph.node_neighbors)
		show_graph(subgraph)
		subgraph.get_degree()
		odd=subgraph.odd_nodes()
		traverse=improved_dfs(subgraph,odd[0])
		print("遍历路径:",traverse)


def improved_dfs(graph,source):
	if source is None:
		print("无节点",source)
		return
	nodeSet = []
	stack = []
	father={}  #记录父节点
	loop=[]    #记录回路
	print("起点为：",source)
	nodeSet.append(source)
	stack.append(source)
	while len(stack) > 0:
		cur = stack.pop()               # 弹出最近入栈的节点
		# if cur in loop:continue
		for next in graph.node_neighbors[cur]:         # 遍历该节点的邻接节点
			if next not in nodeSet:     # 如果邻接节点不重复
				father[next]=cur
				stack.append(cur)       # 把节点压入
				stack.append(next)      # 把邻接节点压入
				nodeSet.append(next)    # 登记节点
				# print("stack",stack)
				# print(next)       		# 打印节点值
				break                   # 退出，保持深度优先
			#elif (next in nodeSet) and (father[cur]!=next): #next被访问过，但不是cur的回溯过程中的父节点
			elif (next in stack) and (father[cur]!=next):
				print("存在回路,起点：",next)
				loop.append(next)
				loop.append(cur)
				nodeSet.append(next)
				temp=cur
				while(father[temp]!=next):#回溯到环的重合点
					# print("father[",temp,"]=",father[temp])
					temp=father[temp]
					loop.append(temp)
				loop.append(next)
				print(loop)
				loop=[]
	return nodeSet

def dfs(graph,node):
	if node is None:
		print("无节点")
		return
	nodeSet = []
	stack = []
	print("起点为：",node)
	nodeSet.append(node)
	stack.append(node)
	while len(stack) > 0:
		cur = stack.pop()               # 弹出最近入栈的节点
		for next in graph.node_neighbors[cur]:         # 遍历该节点的邻接节点
			if next not in nodeSet:     # 如果邻接节点不重复
				stack.append(cur)       # 把节点压入
				stack.append(next)      # 把邻接节点压入
				nodeSet.append(next)    # 登记节点
				# print("stack",stack)
				# print(next)       		# 打印节点值
				break                   # 退出，保持深度优先
	return nodeSet

"""
计算所得路径的方差
"""
def cal_variance(paths):
	avr=0
	varn=0
	for path in paths:
		avr+=cal_length(path)
	avr=avr/len(paths)
	print("平均路径长度",avr)
	for path in paths:
		varn+=math.pow(len(path)-avr,2)
	varn=varn/len(paths)
	print("路径方差：",varn)

def cal_length(path):
	count=0
	for nodes in path:
		if isinstance(nodes,list):
			# for node in nodes:
			# 	count=count+1
			count=count+N+1
		else:
			count=count+1
	return count

if __name__ == '__main__':
	graph_demo=Graph()
	# # list=[11,12,13,14,21,22,23,24,31,32,33,34,41,42,43,44]  #demo
	# # graph_demo.add_nodes(tuple(list)) #list不能被hash，因为list中元素可变
	# # # graph_demo.add_edge(11,22) #添加一条边
	# #
	# edges=[[11,12],[12,13],[13,14],[14,15],[15,16],[16,17],[17,18],[18,11],[21,22],[22,23],[23,24],[24,21],[31,32],[32,33],[33,34],[34,31],[41,42],[42,43],[43,44],[44,41],[11,22],[22,33],[33,44],[12,23],[23,34],[32,43]]
	# # graph_demo.add_edges(edges)
	# # degree=graph_demo.get_degree()
	# # for k,v in degree.items():
	# #     print(k,v)
	# # odd=odd_nodes(graph_demo,degree)
	# # print(odd)
	# # for a in odd:
	# #     print(a)
	# # show_graph(graph_demo)
	#
	# node_list = [11,12,13,14,21,22,23,24,31,32,33,34,41,42,43,44]
	# graph_demo.add_nodes(tuple(node_list))
	#
	# # edges=[['11','12'],['12','13'],['13','14'],['14','11'],['11','21'],['01','11']]
	# # edges = [[11, 12], [12, 13], [13, 14], [14, 11]]


	nodes=[]
	in_edges=[]
	for i in range(1,M+1):
		for j in range(1,N+1):
			node=i*10+j
			nodes.append(node)
			adj_node=i*10+j%N+1
			edge=(node,adj_node)
			in_edges.append(edge)
	print(nodes)
	print(in_edges)
	# 部分topo
	# out_edges=[(13,23),(23,34),(12,22),(22,33),(33,44),(21,32),(32,43),(43,53),(53,64),(42,52),(52,63),(51,62)]
	out_edges=[(13,23),(23,34),(12,22),(22,33),(33,44),(21,32),(32,43),(43,53),(53,64),(42,52),(52,63),(51,62),
			   (38,48),(48,57),(57,67),(18,27),(27,37),(37,47),(47,56),(56,66),(17,26),(26,36),(36,46),(46,55),
			   (16,25)]

	graph_demo.add_nodes(tuple(nodes))
	graph_demo.add_edges(in_edges)
	graph_demo.add_edges(out_edges)
	show_graph(graph_demo)
	print(graph_demo.all_nodes())
	# graph_copy = deep_copy(graph_demo)
	v_path_list = vertical_path(graph_demo, M, N)
	# show_graph(graph_demo)
	odd_list=graph_demo.odd_nodes()
	l_path_list=landscape_path(graph_demo)

	path_list=balanced_combination(v_path_list,l_path_list)

	# path_list=combination(v_path_list,l_path_list)
	get_traverse(path_list)


