import sys
import networkx as nx

# devolve o complemento do literal:
def neg(l):
    # se ~x1 -> x1 
    if l[0] == "~":
        return l.replace("~", "")
    # se x1 -> ~x1    
    return "~" + l

def Resolve_2SAT(G):
    # 1. Lista de CFCs
    CFCs = list(nx.strongly_connected_components(G))

    # comp[v] = índice da CFC que contém o vértice v
    comp = {}
    for i in range(len(CFCs)):
        for node in CFCs[i]:
            comp[node] = i

    # 2. Se x e ~x estão na mesma CFC, é insatisfatível
    for node in G.nodes:
        if node[0] != "~":                  # só olha as variáveis x_i
            if comp[node] == comp[neg(node)]:
                return None                 # Insatisfatível

    # Grafo condensado: cada nó é uma CFC, e "members" guarda os literais
    C = nx.condensation(G, scc=CFCs)

    # Ordem topológica: das fontes para os sorvedouros
    ordem = list(nx.topological_sort(C))
    ordem.reverse()		# Inverte a ordenação para começar pelos sorvedouros
		
    # 3. Nenhum literal atribuído ainda
    valor = {}

    # 4. Percorre as CFCs das fontes para os sorvedouros
    for n in ordem:
        for l in C.nodes[n]["members"]:
            if l not in valor:              # literal ainda não atribuído
                valor[l] = True
                valor[neg(l)] = False

    return valor


# Cria um grafo vazio
G = nx.DiGraph()

for linha in sys.stdin:
    partes = linha.split()
    if len(partes) == 0:
        continue                            # ignora linhas em branco
    a = partes[0]
    b = partes[1]
    # cláusula (a ou b) vira as implicações ~a -> b e ~b -> a
    G.add_edge(neg(a), b)
    G.add_edge(neg(b), a)


resultado = Resolve_2SAT(G)

if resultado is None:
    print("Insatisfatível")
else:
    print("Atribuição encontrada:")
    for node in G.nodes:
        print(node, "=", resultado[node])
