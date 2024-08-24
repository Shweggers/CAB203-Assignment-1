import graphs
import digraphs
import csv


def gamesOK(games):
   edges = games | { (b, a) for (a, b) in games }
   vertices = { a for (a, _) in edges }
   return all(len(graphs.N(vertices, edges, a) & graphs.N(vertices, edges, b)) >= 2 for (a, b) in { (a, b) for a in vertices for b in vertices if a != b and (a, b) not in edges } ) and all(graphs.degree(vertices, edges, a) == graphs.degree(vertices, edges, b) for (a, b) in edges)


def referees(games, refereecsvfilename):
   with open(refereecsvfilename, 'r') as csvfile:
      reader = csv.reader(csvfile); next(reader)
      
      values = { row[0]: set(row[1:]) for row in reader }
      
      maxMatching = { a : b for (a, b) in digraphs.maxMatching(games, values.keys(), { ((a, b), c) for (a, b) in games for c in values.keys() if c not in (a, b) and {a, b}.isdisjoint(values[c]) }) if a in games}
      return maxMatching if len(maxMatching) == len(games) else None


def gameGroups(assignedReferees):
   edgesDirected = { ((a, b), (c, d)) for (a, b) in assignedReferees for (c, d) in assignedReferees if {a, b} - {c, d} and ( (b == d) or (a == c) or assignedReferees[a, b] == assignedReferees[c, d] or assignedReferees[c, d] in (a, b) ) }
   return graphs.colourClassesFromColouring(graphs.minColouring(assignedReferees.keys(), edgesDirected | { (b, a) for (a, b) in edgesDirected })[1])


def gameSchedule(assignedReferees, gameGroups):
   vertices = { frozenset(a) for a in gameGroups }
   topOrdering = digraphs.topOrdering(vertices, { (a, b) for a in vertices for b in vertices if any(r in c and g in b for c in a for g, r in assignedReferees.items()) })
   return topOrdering if topOrdering is None else [ set(a) for a in topOrdering ]


def scores(p, s, c, games):
   pass