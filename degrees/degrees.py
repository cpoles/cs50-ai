import csv
import sys
import time

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
       sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    start_time = time.time()
    path = shortest_path(source, target)
    print(f"{(time.time() - start_time):.6f} seconds", )

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # print("Source: ", source)
    #print("Target: ", target)
    # Keep track of number of states explored
    num_explored = 0

    # Store all possible solutions if any
    solutions = []

    # state is a tuple (movie_id, person_id)

    # Initialize frontier to the starting position
    start = Node(state=(None, source), parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialize empty explored set
    explored = set()

    # Keep looping until solution found
    while True:

        #print("Frontier", frontier.frontier)
        #print()
        # If nothing left in frontier, then no path
        if frontier.empty():
           return None
        
        # Choose a node from the frontier
        node = frontier.remove()
        #print("Current", node.state)
        
        # If node is the goal, then we have a solution
        if node.state[1] == target:
            path = []
            # backtrack to origin
            while node.parent is not None:
                path.append(node.state)
                node = node.parent
            path.reverse()
            # print("Path", path)
            return path
        
        # If node not the goal, Mark node as explored
        explored.add(node.state)
        num_explored += 1
        #print("Explored", explored)

        # get neighbors of the current node
        neighs = neighbors_for_person(node.state[1])
       
        # Optimization

        # check if target is in the neighbours
        if target in [person_id for _, person_id in neighs]:
            # retrieve the corresponding target state
            state = [neigh for neigh in neighs if neigh[1] == target][0]
            # create target node
            child = Node(state=state, parent=node, action=None)
            
            path = []
            # backtrack to origin
            while child.parent is not None:
                path.append(child.state)
                child = child.parent
            path.reverse()
            # print("Path", path)
            return path
        
        # check if the current actor of the node is in the neighbours
        if node.state[1] in [person_id for _, person_id in neighs]:
            # remove neighbours whose actor is equal to the current actor
            # remove any neighbour whose actor is equal to the source actor
            neighs = [neigh for neigh in neighs if node.state[1] != neigh[1] or start.state[1] != neigh[1]]

        #print("Neighbours", neighs)
        # Add neighbours to frontier
        for neigh in neighs:
            # if not yet explored, add to the frontier
            if neigh not in explored and not frontier.contains_state(neigh):
                child = Node(state=neigh, parent=node, action=None)
                frontier.add(child)
   

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
    
