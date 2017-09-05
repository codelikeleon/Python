import random
import matplotlib.pyplot as plt


def main():
    number_of_bins = int(input("Please enter the number of bins: "))
    number_of_items = int(input("Please enter the number of items: "))
    p = int(input("p value: "))

    pheromone_map = generate_pheromone_map(number_of_items, number_of_bins)  # Creates an initial pheromone_map with
    print("Initial Pheromone map =")  # random pheromone values
    print(pheromone_map)
    items = [i * 2 for i in generate_items(number_of_items)]  # i ** 2 or i * 2 for the appropriate BPP
    print("\nItems:")
    print(items)
    number_of_runs = 10000
    fitness_results = []  # Storage for graph points
    count = 0  # Counter used to output percentage complete to terminal

    for n in range(int(number_of_runs / p)):
        ant_paths = []  # Lists used to keep track of paths and their relative fitness so the pheromone_map
        ant_fitness = []  # can be updated with new pheromone values
        evaporate_pheromone(pheromone_map, 0.9)  # Change evaporation to 0.6 or 0.9 depending on BPP

        for i in range(p):
            bin_list = generate_bin_list(number_of_bins)
            path_list = generate_path(pheromone_map, number_of_items)
            ant_paths.append(path_list)
            put_items_in_bins(path_list, items, bin_list)
            fitness = evaluate_fitness(bin_list)
            ant_fitness.append(fitness)

        for i in range(p):
            update_pheromone(pheromone_map, ant_paths[i], ant_fitness[i])  # Update pheromone_map values using
                                                                           # ant_paths and ant_fitness
        fitness_results.append(min(ant_fitness))    # Save minimum fitness value for p number of paths generated
        count += 1
        print(round((count / (number_of_runs / p)) * 100, 2), "% complete")

    print("\nFinal pheromone_map =")
    print(pheromone_map)
    print("\nFitness results: ")
    print(fitness_results)

    plt.plot(fitness_results)   # Plot the best fitness result from p ants onto a graph
    plt.ylabel("Fitness")
    plt.show()


def generate_bin_list(number_of_bins):
    """
    Creates an empty list holding more empty lists for each bin in the BPP. For example, a BPP with 3 bins would
    return the list [[],[],[]]. The weights of the items for each bin are then stored in each list corresponding to its
    bin.

    :param (int) number_of_bins: The number of bins for the BPP

    :return (list) bins: An empty list of number_of_bins number of empty lists
    """
    bins = []
    for i in range(number_of_bins):
        bins.append([])

    return bins


def generate_items(number_of_items):
    """
    Creates a random number of integers between 1 and 500 and returns them as a list. These will be the weights of items
    placed into the bins.

    :param (int) number_of_items: The number of items for the BPP

    :return (list(int)) items: A list containing random item weights as integers
    """
    items = []
    for i in range(number_of_items):
        items.append(random.randint(1, 501))

    return items


def generate_pheromone_map(number_of_items, number_of_bins):
    """
    Creates a 3-Dimensional list representing the construction graph used to model pheromone values. Random pheromone
    values between 0 and 1 are placed into k (where k is in pheromone_map[i][j][k]). i is set used to access the item
    number, j the bin number, and k the link on a graph containing a pheromone value. For example,
    pheromone_map[5][3][7] would be referencing the 8th/[7] pheromone link for the 6th/[5] item to be placed into the
    4th/[3] bin.

    :param (int) number_of_items: The number of items for the BPP
    :param (int) number_of_bins: The number of bins for the BPP

    :return (list) bins: A 3-dimensional list of pheromone value floats
    """
    pheromone_map = []
    for i in range(number_of_items):
        if i == 0:                                  # Root node has less links so is treated differently to the rest
            pheromone_map.append([[]])
            for m in range(number_of_bins):
                pheromone_map[i][0].append(random.uniform(0, 1))        # Insert random pheromone value
        else:
            pheromone_map.append([])
            for j in range(number_of_bins):
                pheromone_map[i].append([])
                for k in range(number_of_bins):
                    pheromone_map[i][j].append(random.uniform(0, 1))    # Insert random pheromone value
    return pheromone_map


def choose_pheromone_path(pheromone):
    """
    Takes an array of pheromone and returns the index of the chosen pheromone path within that list, relative to the
    current node. A pheromone value is chosen by random selection, biased towards pheromones of a higher value. The
    random selection method is a form of to roulette wheel selection.

    :param (list(float)) pheromone: A list of floating point pheromone values

    :return (int) count: The index of the chosen pheromone value.
    """

    total_pheromone = 0
    for i in pheromone:
        total_pheromone += i

    selection = random.uniform(0, total_pheromone)

    count = 0
    pheromone_pile = 0
    for i in pheromone:
        pheromone_pile += i
        if selection < pheromone_pile:  # Once the pheromone_pile is larger than the selection, the last pheromone value
            return count                # added to the pile is the chosen value.
        count += 1


def generate_path(pheromone_map, number_of_items):
    """
    Generates a path by moving through the pheromone_map, placing the indices of selected pheromone values into
    path_list. number_of_items == len(pheromone_map) but is used to improve the code readability.

    :param (list) pheromone_map: The 3-dimensional list holding all pheromone values
    :param (int) number_of_items: The number of items for the BPP

    :return (list) path_list: a list containing the indices of chosen pheromone values, contributing to a path across
                              the construction graph
    """

    path_list = [choose_pheromone_path(pheromone_map[0][0])]    # Exclude root node from loop as it has fewer pheromones

    for i in range(number_of_items - 1):
        next_path = choose_pheromone_path(pheromone_map[i + 1][path_list[i]])  # This helps keep track of the order of
        path_list.append(next_path)                                            # bins.

    return path_list


def put_items_in_bins(path_list, items, bin_list):
    """
    Uses the indices in path_list as a reference to which bin to place an item into. A path_list of [0, 1, 4] would
    place the first item into bin 0, the second into bin 1, and last into bin 4.

    :param (list(int)) path_list: A list containing the indices of the bins in which to put the items
    :param (list(int)) items: A list of items represented as integers corresponding to their weight
    :param (list) bin_list: A list containing empty lists representing bins

    :return: This function does not return any value
    """

    count = 0
    for i in path_list:
        bin_list[i].append(items[count])    # Place the item into the correct bin based on the index specified in
        count += 1                          # path_list


def evaluate_fitness(bin_list):
    """
    Fitness is evaluated as the difference between the heaviest and lightest bins. A lower value means a better fit.

    :param (list) bin_list: A list containing empty lists representing bins

    :return (int) difference: The difference between the heaviest and lightest bins. This is a measure of fitness
    """

    bin_total_weights = []
    for i in range(len(bin_list)):
        total = sum(bin_list[i])  # Calculate total weight in each bin
        bin_total_weights.append(total)

    heaviest_bin = max(bin_total_weights)   # Find largest total bin weight
    lightest_bin = min(bin_total_weights)   # Find smallest total bin weight
    difference = heaviest_bin - lightest_bin

    return difference


def evaporate_pheromone(pheromone_map, evaporation_rate):
    """
    Multiplies all pheromone values in pheromone_map by the evaporation_rate.

    :param (list) pheromone_map: The 3-dimensional list holding all pheromone values
    :param (float) evaporation_rate: The specified evaporation rate between 0 and 1

    :return: This function does not return any value
    """

    pheromone_map[0][0] = [pheromone * evaporation_rate for pheromone in
                           pheromone_map[0][0]]  # Evaporate root node links seperately as it contains fewer pheromones

    for i in range(1, len(pheromone_map)):    # Loop through the remaining pheromone values
        for j in range(len(pheromone_map[1])):
            pheromone_map[i][j] = [pheromone * evaporation_rate for pheromone in
                                   pheromone_map[i][j]]  # Evaporate all other pheromone values


def update_pheromone(pheromone_map, path_list, fitness):
    """
    Updates the pheromone values of the chosen path in pheromone_map.

    :param (list) pheromone_map: The 3-dimensional list holding all pheromone values
    :param (list(int)) path_list: A list containing the indices of the bins in which to put the items
    :param (int) fitness: The difference between the heaviest and lightest bins

    :return: This function does not return any value
    """

    if fitness == 0:
        additional_pheromone = 1000  # If optimal solution is found, +1000 pheromone to avoid division by 0
    else:
        additional_pheromone = 100 / fitness

    pheromone_map[0][0][path_list[0]] += additional_pheromone  # Separate root node again, add additional pheromone by
    prev_path = path_list[0]    # Keep track of previous pheromone to differentiate between bins

    for i in range(1, len(pheromone_map)):
        pheromone_map[i][prev_path][path_list[i]] += additional_pheromone   # Follow path_list for the remaining links
        prev_path = path_list[i]


main()
