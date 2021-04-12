#!/usr/bin/env python
# coding: utf-8

# In[428]:


import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# In[429]:


# def dfs(v, graph, used):
#     used[v] = 1
#     for to in graph[v]:
#         if used[to] == 0:
#             dfs(to, graph, used)

# def get_min_max_degrees(graph):
#     min_d = len(graph)
#     max_d = 0
#     for i in range(len(graph)):
#         d = len(graph[i])
#         if d < min_d:
#             min_d = d
#         if d > max_d:
#             max_d = d
#     print('Мин и макс степени: ', min_d, max_d)



# def create_random_graph(n):
#     min_degree = 2
#     max_degree = 4 
#     degree = []
#     sum_degrees = 0
#     for i in range(n):
#         d = random.randint(min_degree, max_degree)
#         degree.append(d)
#         sum_degrees += d

#     #degree = [4, 3, 2, 4, 2, 3, 3, 4, 4, 4]
#     #print(sum_degrees)
#     #print(degree)
#     graph = [[] for i in range(n)]
#     edges = [set() for i in range(n)]
#     num_ver = n
#     num_itr = 0 
    
#     while num_ver > 1:
#         p = [d / sum_degrees for d in degree]
#         #print(p)
#         v, u = np.random.choice(n, 2, p=p)
#         num_itr = 0
#         while (v == u or v in edges[u]) and num_itr < 10:
#             v, u = np.random.choice(n, 2, p=p)
#         if num_itr == 10:
#             break
            
#         #print(v, u)
#         degree[v] -= 1
#         if degree[v] == 0:
#             num_ver -= 1
#         degree[u] -= 1
#         if degree[u] == 0:
#             num_ver -= 1
#         graph[v].append(u)
#         graph[u].append(v)
#         edges[v].add(u)
#         edges[u].add(v)
#         sum_degrees -= 2
#         #print(degree)
        
#     #print(2)   
#     used = [0 for i in range(n)]
#     comp = 0
#     prev = 0
#     for i in range(n):
#         if used[i] == 0:
#             comp += 1
#             dfs(i, graph, used)
#             if i != prev:
#                 graph[prev].append(i)
#                 graph[i].append(prev)
#             prev = i

# #     small_degree = []
# #     for i in range(n):
# #         if len(g[i]) < min_degree:
# #             small_degree.append(i)
# #     for i in range(small)
    
#     get_min_max_degrees(graph)
#     return graph


# In[430]:


class Node:
    def __init__(self, id_, k):
        self.id_ = id_
        self.k = k
        self.hash_table = []
        self.files = set()
        
    def get_bucket_ind(self, key):
        xor = self.id_ ^ key
        ind = 0
        while (1 << (ind + 1)) <= xor :
            ind += 1
        return ind
    
    def get_k_bucket(self, key):
        if key in self.files or self.id_ == key:
            return 1, []
        
        i_bucket = self.get_bucket_ind(key)
        bucket = []
        dist = self.id_^key
        while len(bucket) < self.k and i_bucket >= 0:
            for node in self.hash_table[i_bucket]:
                if dist > node[-1]^key:
                    bucket.append((key^node[-1], node[0]))
            i_bucket -= 1
        bucket.sort()
        while len(bucket) > self.k:
            bucket.pop()
        return 0, bucket


# In[431]:


class Network:
    
    def print_key(self, id_, fl=1):
        s = ''
        a = 1
        while a <= self.max_id:
            if a & id_ > 0:
                s = '1' + s
            else:
                s = '0' + s
            a <<= 1
        if fl == 1:
            print(id_, s)
        else:
            return s 
              
    def print_node(self, i):
        id_ = self.nodes[i].id_
        s = self.print_key(id_, 0)
        print(i, id_, s)

        
    def __create_nodes(self):
        self.nodes = []
        self.node_ids = set()
        self.node_id_map = {}
        for i_node in range(self.n):
            cur_id = random.randint(1, self.max_id)
            while cur_id in self.node_ids:
                cur_id = random.randint(1, self.max_id)
            self.nodes.append(Node(cur_id, self.k))
            self.node_ids.add(cur_id)
            self.node_id_map[cur_id] = i_node
#         for i in range(self.n):
#             self.print_node(i)
            
            
    def __create_graph(self):
        self.graph = [[] for i in range(self.n)]
        for i_node in range(self.n):
            self.nodes[i_node].hash_table = [[] for i in range(self.hash_size + 1)]
            id_ = self.nodes[i_node].id_
            node_ids = [(self.nodes[i].id_^id_, i) for i in range(self.n)]
            node_ids.sort()
            ind = 0
            max_dist = 2
            i_bucket = 0
#             print(i_node, node_ids)
            while max_dist <= (1 << self.hash_size) and ind < self.n:
                cur_nodes = []
                while ind + 1 < self.n and node_ids[ind + 1][0] < max_dist:
                    ind += 1
                    cur_nodes.append(node_ids[ind][-1])
                if len(cur_nodes) > 0:
                    to = cur_nodes[random.randint(0, len(cur_nodes)-1)]
                    #print(len(self.nodes), i_node)
                    #print(len(self.nodes[i_node].hash_table))
                    self.nodes[i_node].hash_table[i_bucket].append((to, self.nodes[to].id_))
                    self.graph[i_node].append(to)
                max_dist <<= 1
                i_bucket += 1
#             print(i_node, self.nodes[i_node].hash_table)
                
            
#     def __fill_hash_tables(self):
#         #print('----------------------------')
#         for i_node in range(self.n):
#             self.nodes[i_node].hash_table = [[] for i in range(self.hash_size + 1)]
#             #print(fr)
#             for to in self.graph[i_node]:
#                 i_bucket = self.nodes[i_node].get_bucket_ind(self.nodes[to].id_)
#                 self.nodes[i_node].hash_table[i_bucket].append((to, self.nodes[to].id_))
#                 #print('--')
                
                
    def __add_files(self):
        self.file_ids = set()
        for i_file in range(10*self.n):
            file_id = random.randint(1, self.max_id-1)
            while file_id in self.node_ids or file_id in self.file_ids:
                file_id = random.randint(1, self.max_id-1)
            self.file_ids.add(file_id)
            i = random.randint(1, self.n-1)
            self.nodes[i].files.add(file_id)
            
            dist_node = [(file_id^self.nodes[i_node].id_, i_node) for i_node in range(len(self.nodes))]
            dist_node.sort()
            #print(dist_node)
            for i_node in range(1):
                self.nodes[dist_node[i_node][-1]].files.add(file_id)
                
    
    def find_key(self, this, key):
        min_buck_sz = n
        max_buck_sz = 0
        avg_buck_sz = 0
        num = 0
        path = [this]
        #self.print_key(key)
        self.used = set()
        self.used.add(this)
        #self.print_node(this)
        res, bucket = self.nodes[this].get_k_bucket(key)
        if len(bucket) == 0:
            return res, path, 0, 0, 0
        best_dist = bucket[0][0]+1
        
        while len(bucket) > 0:
            if bucket[0][0] > best_dist:
                return 0, path, min_buck_sz, max_buck_sz, avg_buck_sz / num
            else:
                best_dist = bucket[0][0]
            cur_node = bucket[0][-1]
            num += 1
            path.append(cur_node)
            #self.print_node(cur_node)
            self.used.add(cur_node)
            res, new_bucket = self.nodes[cur_node].get_k_bucket(key)
            if res == 1:
                return res, path, min_buck_sz, max_buck_sz, avg_buck_sz / num
            sz = len(new_bucket)
            min_buck_sz = min(min_buck_sz, sz)
            max_buck_sz = max(max_buck_sz, sz)
            avg_buck_sz += sz
            bucket_set = set()
            for item in bucket:
                if not item[-1] in self.used:
                    bucket_set.add(item)
            for item in new_bucket:
                if not item[-1] in self.used:
                    bucket_set.add(item)
            bucket =  sorted(bucket_set)
            while len(bucket) > self.k:
                bucket.pop()
                
        return 0, path, min_buck_sz, max_buck_sz, avg_buck_sz / num
            
        
    def __init__(self, n):
        self.n = n
        self.k = 3
        #self.graph = graph
        self.max_id = self.n*self.n
        #self.max_id = 10000
        self.hash_size = 1
        while (1 << self.hash_size) < self.max_id:
            self.hash_size += 1
        #print(self.graph)
        self.__create_nodes()
        self.__create_graph()
        #self.__fill_hash_tables()
        #for node in self.nodes:
        #    print(node.id_, node.hash_table)
        self.__add_files()
        
    def get_degrees(self):
        min_d = self.n
        max_d = 0
        avg_d = 0
        for node in self.nodes:
            d = 0
            for bucket in node.hash_table:
                d += len(bucket)
            min_d = min(min_d, d)
            max_d = max(max_d, d)
            avg_d += d
        avg_d /= self.n
#         print('Минимальная степень вершины: ', min_d)
#         print('Максимальная степень вершины: ', max_d)
#         print('Средняя степень вершины: ', avg_d)
        return min_d, max_d, avg_d

    def get_files_num(self):
        min_num = self.n*self.n
        max_num = 0
        avg_num = 0
        for node in self.nodes:
            num = len(node.files)
            min_num = min(min_num, num)
            max_num = max(max_num, num)
            avg_num += num
        avg_num /= len(self.nodes)
        return min_num, max_num, avg_num

          
    def draw_path(self, path, file_key):
        plt.figure(figsize=(30, 20))
        graph = nx.DiGraph()
        for fr in range(self.n):
            for to in self.graph[fr]:
                graph.add_edge(self.nodes[fr].id_, self.nodes[to].id_)
                
        node_map = [0 for i in range(self.n)]
        #print(graph.nodes)
        ind = 0
        for node in graph.nodes:
            node_map[self.node_id_map[node]] = ind
            ind += 1
        node_colors=['deepskyblue' for i in range(graph.number_of_nodes())]
        for i in range(self.n):
            if file_key in self.nodes[i].files:
                node_colors[node_map[i]]='lawngreen'
        pos = nx.kamada_kawai_layout(graph)
        f = plt.figure()
        
        prev_node = -1
        for i in range(len(path)):
            node = path[i]
            if i < len(path) - 1:
                node_colors[node_map[node]]='deeppink'
            else:
                node_colors[node_map[node]]='orangered'
            nx.draw(graph, with_labels=True, pos=pos, node_color=node_colors)
            img_name = 'graph'+str(i)+'.png'
            plt.savefig(img_name, format='PNG')
            f.clear()
            prev_node = node


# In[427]:


def draw():
    t = 0
    flag = 0
    while t < 1000 and not flag:
        n = 15
        network = Network(n)
        node = random.randint(0, n-1)
        files = list(network.file_ids)
        file = files[random.randint(0, len(files)-1)]
        res, path, min_buck_sz, max_buck_sz, avg_buck_sz = network.find_key(node, file)
        if len(path) > 3:
            network.draw_path(path, file)
            print(file)
            flag = 1


# In[383]:


def get_statistics():
    n_networks = 10
    n = 1000
    min_degree = n
    max_degree = 0
    avg_degree = 0
    min_files = n*n
    max_files = 0
    avg_files = 0
    min_len = n
    max_len = 0
    avg_len = 0
    min_buck = n
    max_buck = 0
    avg_buck = 0
    for i_network in range(n_networks):
        network = Network(n)
        min_d, max_d, avg_d = network.get_degrees()
        min_degree = min(min_degree, min_d)
        max_degree = max(max_degree, max_d)
        avg_degree += avg_d
        min_f, max_f, avg_f = network.get_files_num()
        min_files = min(min_files, min_f)
        max_files = max(max_files, max_f)
        avg_files += avg_f
        for i in range(n):           
            node = i
            files = list(network.file_ids)
            file = files[random.randint(0, len(files)-1)]
            # if random.random() < 0.5:
            #     file = random.randint(0, n*n-1)
            res, path, min_buck_sz, max_buck_sz, avg_buck_sz = network.find_key(node, file)
            path_len = len(path)
            min_len = min(min_len, path_len)
            max_len = max(max_len, path_len)
            avg_len += path_len
            min_buck = min(min_buck, min_buck_sz)
            max_buck = max(max_buck, max_buck_sz)
            avg_buck += avg_buck_sz
    avg_degree /= n_networks
    avg_files /= n_networks
    avg_len /= n * n_networks
    avg_buck /= n * n_networks
    print('Мин./ср./макс. степень вершины: ', min_degree, '/', avg_degree, '/', max_degree)
    print('Мин./ср./макс. количество файлов: ', min_files, '/', avg_files, '/', max_files)
    print('Мин./ср./макс. длина пути: ', min_len, '/', avg_len, '/', max_len)
    print('Мин./ср./макс. размер сообщения: ', min_buck, '/', avg_buck, '/', max_buck)


# In[384]:


# get_statistics()
# draw()


# In[432]:


n = 1000
network = Network(n)
node = random.randint(0, n-1)
files = list(network.file_ids)
file = files[random.randint(0, len(files)-1)]
res, path, min_buck_sz, max_buck_sz, avg_buck_sz = network.find_key(node, file)


# In[ ]:




