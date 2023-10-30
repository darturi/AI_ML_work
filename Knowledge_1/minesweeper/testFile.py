cell = (7,7)
height = 8
width = 8
moves_made = [(1,1)]

moves_made.append(cell)
adj_cells = []
for i in range((cell[0] - 1), (cell[0] + 2)):
    for j in range((cell[1] - 1), (cell[1] + 2)):
        if (i >= 0) and (i <= (width-1)) and (j >= 0) and (j <= (height-1)) and (i, j) not in moves_made:
            adj_cells.append((i, j))

print(adj_cells)

#print(type(s1_ex.cells))
#print(sentence1.cells.issubset(sentence2))
#for cell in s1_ex.cells:
#    print(cell)