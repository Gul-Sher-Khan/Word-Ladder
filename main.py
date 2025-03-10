import heapq
import random
import networkx as nx
import matplotlib.pyplot as plt

def setup_words(length, word_list):
   words = []
   for word in word_list:
        if len(word) == length:
             words.append(word)
   return words

def check(a, b):
    """Return True if words a and b differ by exactly one letter."""
    diff = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            diff += 1
        if diff > 1:
            return False
    return diff == 1

def createGraph(word_list):
    """Create a graph where each word is a node connected to words that differ by one letter."""
    graph = {}
    for word in word_list:
        graph[word] = []
        for other in word_list:
            if word != other and check(word, other):
                graph[word].append(other)
    return graph

def bfs(graph, start, end):
    """Breadth-First Search to find a valid transformation path."""
    queue = [[start]]
    visited = set()
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                new_path = path[:] + [neighbor]
                queue.append(new_path)
    return None

def ucs(graph, start, end):
    """Uniform Cost Search (UCS) to find the shortest path from start to end."""
    priority_queue = []
    heapq.heappush(priority_queue, (0, [start]))  # (cost, path)
    visited = set()

    while priority_queue:
        cost, path = heapq.heappop(priority_queue)
        node = path[-1]

        if node in visited:
            continue
        visited.add(node)

        # If we reach the end, return the path and cost
        if node == end:
            return path, cost

        # Expand neighbors
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (cost + 1, path + [neighbor]))

    return None, float('inf')  # Return None if no path is found

def heuristic(a, b):
    count = 0

    for i in range(len(a)):
        if a[i] != b[i]:
            count *= 5

    return count

def a_star(graph, start, end):
    frontier = []
    g = 0
    f = g + heuristic(start, end)
    heapq.heappush(frontier, (f, g, [start]))
    visited = {}
    while frontier:
        f, g, path = heapq.heappop(frontier)
        node = path[-1]
        if node == end:
            return path
        if node in visited and visited[node] <= g:
            continue
        visited[node] = g
        for neighbor in graph[node]:
            new_g = g + 1
            new_f = new_g + heuristic(neighbor, end)
            new_path = path + [neighbor]
            heapq.heappush(frontier, (new_f, new_g, new_path))
    return None

def ai_assistance(start, target, graph):
    print("\nSelect the algorithm you want to use for AI Assistance:")
    print("1. Breadth-First Search")
    print("2. Uniform Cost Search")
    print("3. A* Search")

    choice = input("\nEnter 1, 2, or 3: ")

    if choice not in ["1", "2", "3"]:
        print("Invalid input.")
        return
    
    if choice == "1":
        path = bfs(graph, start, target)
        if path:
            print("The next move is:", path[1])
        else:
            print("No valid transformation path found.")
    
    elif choice == "2":
        path = ucs(graph, start, target)
        if path:
            print("The next move is:", path[1])
        else:
            print("No valid transformation path found.")
    
    elif choice == "3":
        path = a_star(graph, start, target)
        if path:
            print("The next move is:", path[1])
        else:
            print("No valid transformation path found.")

def game(start, target, graph, word_length, word_list):
    print(f"Transform {start} into {target} in the fewest steps possible.")

    score = 100
    moves = 0
    while True:
        print(f"\nCurrent word: {start}")
        print(f"Score: {score} | Moves: {moves}")
        
        print("\nDo you want AI assistance?")
        print("1. Continue Manually")
        print("2. Get AI Assistance")

        choice = input("Enter 1 or 2: ")

        if choice not in ["1", "2"]:
            print("Invalid input")
            continue

        if choice == "2":
            ai_assistance(start, target, graph)
            continue
        
        pos = int(input(f"Choose Letter Position to Change (1-{word_length}): "))
        if pos < 1 or pos > word_length:
            print("Invalid position! Choose a valid number.")
            continue
        new_letter = input("Enter New Letter: ").lower()
        if len(new_letter) != 1 or not new_letter.isalpha():
            print("You must enter a single alphabet letter!")
            continue

        temp = start[:pos-1] + new_letter + start[pos:]
        if temp in word_list and temp in graph[start]:
            start = temp
            moves += 1
            score -= 5  # Deduct points per move
        else:
            print("Wrong Move! Either the word is invalid or it is not a one-letter change. Try again.")
            continue
        
        if start == target:
            print("\nCongratulations! You Won!")
            print(f"Final Score: {score} | Total Moves: {moves}")
            break    

def game_challenge(start, target, graph, word_length, word_list):
    move_limit = 10
    moves = 0
    score = 100

    potential_banned = []

    # Add words to potential_banned if they are not the current or target word
    for word in word_list:
        if word != start and word != target:
            potential_banned.append(word)

    if len(potential_banned) >= 3:
        banned_count = 3
    else:
        banned_count = len(potential_banned)

    banned_words = []
    if banned_count > 0:
        banned_words = random.sample(potential_banned, banned_count)

    print("\n*** Challenge Mode ***")
    print(f"Transform {start} into {target} in the {move_limit} steps")
    print("Obstacles:")
    if banned_words:
        print("Banned words (cannot be used):", ", ".join(banned_words))
    
    while moves < move_limit:
        print(f"\nCurrent word: {start}")
        print(f"Score: {score} | Moves: {moves}")

        print("\nDo you want AI assistance?")
        print("1. Continue Manually")
        print("2. Get AI Assistance")

        choice = input("Enter 1 or 2: ")

        if choice not in ["1", "2"]:
            print("Invalid input")
            continue

        if choice == "2":
            ai_assistance(start, target, graph)
            continue

        pos = int(input(f"Choose Letter Position to Change (1-{word_length}): "))

        if pos < 1 or pos > word_length:
            print("Invalid position! Choose a valid number.")
            continue

        new_letter = input("Enter New Letter: ").lower()

        if len(new_letter) != 1 or not new_letter.isalpha():
            print("You must enter a single alphabet letter!")
            continue

        temp = start[:pos-1] + new_letter + start[pos:]

        if temp in word_list and temp in graph[start] and temp not in banned_words:
            start = temp
            moves += 1
            score -= 5
        else:
            print("Wrong Move! Either the word is invalid, it is not a one-letter change, or it is a banned word. Try again.")
            continue

        if start == target:
            print("\nCongratulations! You Won!")
            print(f"Final Score: {score} | Total Moves: {moves}")
            break

        if moves == move_limit:
            print("\nGame Over! You have reached the maximum number of moves.")
            print(f"Final Score: {score} | Total Moves: {moves}")
            break
          
def multiplayer_mode(start, target, graph, word_length, word_list):
    player1 = input("Enter Player 1 name: ").strip() or "Player 1"
    player2 = input("Enter Player 2 name: ").strip() or "Player 2"
    players = {
        player1: {"current": start, "moves": 0, "score": 100},
        player2: {"current": start, "moves": 0, "score": 100}
    }

    while True:
        for player in players:
            print(f"\n{player}'s Turn")
            print(f"Current word: {players[player]['current']}")
            print(f"Score: {players[player]['score']} | Moves: {players[player]['moves']}")

            print("\nDo you want AI assistance?")
            print("1. Continue Manually")
            print("2. Get AI Assistance")

            choice = input("Enter 1 or 2: ")

            if choice not in ["1", "2"]:
                print("Invalid input")
                continue

            if choice == "2":
                ai_assistance(players[player]['current'], target, graph)
                continue

            pos = int(input(f"Choose Letter Position to Change (1-{word_length}): "))
            if pos < 1 or pos > word_length:
                print("Invalid position! Choose a valid number.")
                continue

            new_letter = input("Enter New Letter: ").lower()
            if len(new_letter) != 1 or not new_letter.isalpha():
                print("You must enter a single alphabet letter!")
                continue

            temp = players[player]['current'][:pos-1] + new_letter + players[player]['current'][pos:]

            if temp in word_list and temp in graph[players[player]['current']]:
                players[player]['current'] = temp
                players[player]['moves'] += 1
                players[player]['score'] -= 5

                if players[player]['current'] == target:
                    print(f"\n{player} Wins!")
                    print(f"Final Score: {players[player]['score']} | Total Moves: {players[player]['moves']}")
                    break
            else:
                print("Wrong Move! Either the word is invalid or it is not a one-letter change. Try again.")
                continue

def visualize_graph(graph):
    # Create a NetworkX graph object
    G = nx.Graph()
    # Add edges from your graph dictionary
    for word, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(word, neighbor)
    
    # Draw the graph with labels
    nx.draw(G, with_labels=True, node_size=500, font_size=8)
    plt.title("Word Transformation Graph")
    plt.show()
    
def main():
    with open("words.txt", "r") as file:
        file_word_list = file.read().splitlines()

    word_list = []

    for word in file_word_list:
        temp = word.split()
        if(temp) != "":
            word_list.append(word.lower())

   
    print("\nChoose Difficulty:")
    print("1. Basic (3-letter words)")
    print("2. Advanced (5-letter words)")

    difficulty = input("Enter 1 or 2: ")
    
    if difficulty not in ["1", "2"]:
        print("Invalid input. Exiting...")
        return
    
    if difficulty == "1":
        word_length = 3
    else:
        word_length = 5
    
    word_list = setup_words(word_length, word_list)

    graph = createGraph(word_list)

    show_graph = input("Do you want to see the word graph visualization? (y/n): ")
    if show_graph.lower() == "y":
        visualize_graph(graph)


    print("\nChoose Game Mode:")
    print("1. Simple Challenge")
    print("2. Challenge Mode")
    print("3. Multiplayer Mode (Live Competition)")

    choice = input("Enter 1, 2, or 3: ")

    if choice not in ["1", "2", "3"]:
        print("Invalid input. Exiting...")
        return
    
    if choice == "1":
        path = None
        while not path:
            start = random.choice(list(graph.keys()))
            target = random.choice(list(graph.keys()))
            if start == target:
                continue
            path = bfs(graph, start, target) 
        game(start, target, graph, word_length, word_list)
    elif choice == "2":
        path = None
        while not path:
            start = random.choice(list(graph.keys()))
            target = random.choice(list(graph.keys()))
            if start == target:
                continue
            path = bfs(graph, start, target)
        game_challenge(start, target, graph, word_length, word_list)
    elif choice == "3":
        path = None
        while not path:
            start = random.choice(list(graph.keys()))
            target = random.choice(list(graph.keys()))
            if start == target:
                continue
            path = bfs(graph, start, target)
        multiplayer_mode(start, target, graph, word_length, word_list)
    else:
        print("Invalid input. Exiting...")
        return    

if __name__ == "__main__":
    main()