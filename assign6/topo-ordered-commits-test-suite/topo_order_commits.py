import os
import sys
import zlib
import copy
import re
from collections import deque

def get_git_directory():
    #get current path
    currentPath = os.getcwd()
    #check if git exist
    while (not os.path.exists(currentPath+'/.git')):
        #if loop reaches root, stderr"
        if(currentPath == '/'):
            sys.stderr.write('Not inside a git repository\n')
            sys.exit()
        #go to parent
        currentPath = os.path.dirname(currentPath)
    #return path of git
    return currentPath+'/.git'

def get_branch_names(git_directory):
    #create a dictionary
    namelist = {}
    #walk through the git directory and find its branch
    for (root,dirs,files) in os.walk(git_directory+'/refs/heads'):
        #Add each branch to dictionary
        for x in files:
            f = open(root+'/'+x,'r')
            #check naming
            key = root[len(git_directory+'/refs/heads')+1:]
            if(key == ''):
                key = x
            else:
                key = key+'/'+x
            namelist[key] = f.read()[:-1]
            f.close()
    #return dictionary
    return namelist

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

#Pseudocode hint given by TA
def build_commit_graph(git_directory, branch_names):
    #get branch hashes
    local_branch_heads = []
    for name in branch_names:
        local_branch_heads.append(branch_names[name])
    #commit graph
    commit_nodes = {}
    visited = set()
    stack = local_branch_heads
    while stack:
        commit_hash = stack.pop()
        #go next commit if already visited
        if commit_hash in visited:
            continue
        visited.add(commit_hash)
        #create new Commit Node if commit not recorded
        if commit_hash not in commit_nodes:
            commit_nodes[commit_hash] = CommitNode(commit_hash)
        commit = commit_nodes[commit_hash]
        #open decode the commit
        f = open(git_directory+'/objects/'+ commit_hash[0:2]+'/'+commit_hash[2:],'rb')
        decoded = zlib.decompress(f.read()).decode()
        #Use regex to get the parent hash
        compiled = re.compile(r'parent \w*').findall(decoded)
        for x in range(len(compiled)):
            compiled[x] = compiled[x][7:]
        commit.parents = compiled
        #record all parents
        for p in commit.parents:
            if p not in visited:
                stack.append(p)
            if p not in commit_nodes:
                commit_nodes[p] = CommitNode(p)
            commit_nodes[p].children.add(commit_hash)
    return commit_nodes

#Pseudocode hint given by TA
def sort_commit_graph(commit_nodes):
    result = []
    no_children = deque()
    copy_graph = copy.deepcopy(commit_nodes)
    for commit_hash in copy_graph:
        if(len(copy_graph[commit_hash].children)==0):
            no_children.append(commit_hash)
    while(len(no_children) > 0):
        commit_hash = no_children.popleft()
        result.append(commit_hash)
        for parent_hash in list(copy_graph[commit_hash].parents):
            copy_graph[commit_hash].parents.remove(parent_hash)
            copy_graph[parent_hash].children.remove(commit_hash)
            if (len(copy_graph[parent_hash].children) == 0):
                no_children.append(parent_hash)
    if (len(result) < len(commit_nodes)):
        raise Exception("cycle detected")
    return result

#Pseudocode hint given by TA
def print_sorted_order(commit_nodes, topo_ordered_commits, head_to_branches):
    jumped = False
    for i in range(len(topo_ordered_commits)):
        commit_hash = topo_ordered_commits[i]
        if jumped:
            jumped = False
            sticky_hash = ' '.join(commit_nodes[commit_hash].children)
            print(f'={sticky_hash}')
        branches = sorted(head_to_branches[commit_hash]) if commit_hash in head_to_branches else []
        print(commit_hash + (' ' + ' '.join(branches) if branches else ''))
        if i + 1 < len(topo_ordered_commits) and topo_ordered_commits[i + 1] not in commit_nodes[commit_hash].parents:
            jumped = True
            sticky_hash = ' '.join(commit_nodes[commit_hash].parents)
            print(f'{sticky_hash}=\n')


def topo_order_commits():
    #Get git directory (can be helper function)
    git_directory = get_git_directory()
    #Get list of local branch names (can be helper function)
    branch_names = get_branch_names(git_directory)
    #Build the commit graph (can be helper function)
    commit_nodes = build_commit_graph(git_directory, branch_names)
    #Topologically sort the commit graph (can be helper fnction)
    topo_commit_graph = sort_commit_graph(commit_nodes)
    head_to_branches = {}
    for name in branch_names:
        head_to_branches[branch_names[name]] = head_to_branches.get(branch_names[name],[])
        head_to_branches[branch_names[name]].append(name)
    #Print the sorted order (can be helper function)
    print_sorted_order(commit_nodes, topo_commit_graph, head_to_branches)

#No git command used

if __name__ == '__main__':
    topo_order_commits()
    
