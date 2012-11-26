from random import choice


def generate_edges(l,r):
	''' takes a list of vertices and a list of edges to be removed r 			and generates the list of edges to be used '''
	edges = []
	for f in l:
		for t in l:
			edges.append((f,t))
	if r:
		return [t for t in edges if t not in r and tuple(reversed(t)) not in r]
	else:
		return edges

def decide_pairs(v,e):
	''' takes a list of unique vertices v and a list of edges in the form of
		tuples (from,to)

		returns a chosen list of edges form of tuples (from,to) '''
	used = []
	def helper(first,p_moves):
		if p_moves:
			second = choice(p_moves)
		else:
			return [(first,None)]
		used.append(second)
		p_moves = [y for (x,y) in e if x == second and y not in used]
		return helper(second,p_moves) + [(first,second)]
	r = helper(None,v)
	temp = r + [([x if y == None else y for x,y in r if x == None or y == None])]
	return [t for t in temp if None not in t]	


if __name__ == "__main__":
	l = ["Andrew Miller","Becky Miller","Katy Miller","Eliz Miller"]
	r = [('Andrew Miller','Eliz Miller')]
	print decide_pairs(l,generate_edges(l,r))
