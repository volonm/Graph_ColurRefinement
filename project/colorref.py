import os
from graph import Graph, Vertex
from graph_io import load_graph, write_dot


def basic_colorref(path):
    try:
        with open(path) as f:
            G, properties = load_graph(f, Graph, read_list=True)

        graph_dict = {}
        colors_graphs = {}
        graph_iteration = {}
        for index, file_graph in enumerate(G):
            print_graph(file_graph, f"{index}_BEFORE")
            iteration = colorref(file_graph)
            graph_dict[index] = file_graph
            graph_iteration[index] = iteration
            print_graph(file_graph, f"{index}_AFTER")

        separate_groups = {}
        for graph_index, value in graph_dict.items():
            colors = tuple(get_all_colors(graph_dict.get(graph_index)))
            # print(f"{graph_index} + \t {colors}")
            same_links = False
            if colors in colors_graphs.keys():
                graphs = colors_graphs[colors]
                for gr_index in graphs:
                    # print(f"Comparing {graph_index} and {gr_index}")
                    if are_perfectly_edged(graph_dict[gr_index].edges, graph_dict[graph_index].edges):
                        same_links = True
                if same_links:
                    colors_graphs[colors].append(graph_index)
                else:
                    separate_groups[len(separate_groups)] = graph_index
            else:
                colors_graphs[colors] = [graph_index]

        res = []
        for colors, group in colors_graphs.items():
            discrete = len(colors) == len(set(colors))
            iteration = graph_iteration[group[0]]
            res.append((group, iteration, discrete))

        # check and add the separate graph groups
        if len(separate_groups.keys()) == 1:
            g_index = separate_groups[separate_groups.keys()[0]]
            discrete = len(get_all_colors(graph_dict[g_index])) == len(set(get_all_colors(graph_dict[g_index])))
            res.append(([g_index], graph_iteration[g_index], discrete))
        elif len(separate_groups.keys()) > 1:
            for g1 in separate_groups.values():
                temporary_group = [g1]
                for g2 in separate_groups.values():
                    if (g1 != g2) and are_perfectly_edged(graph_dict[g1].edges, graph_dict[g2].edges):
                        temporary_group.append(g2)
                if len(temporary_group) > 0:
                    vertexes = get_all_colors(graph_dict[g1])
                    discrete = len(vertexes) == len(set(vertexes))
                    temporary_group = list(sorted(set(temporary_group)))
                    tuple_group_res = (temporary_group, graph_iteration[temporary_group[0]], discrete)
                    if tuple_group_res not in res:
                        res.append(tuple_group_res)

        # Printing the results
        print("Sets of possibly isomorphic graphs:")
        for tuple_res in res:
            if tuple_res[2]:
                print(f"{tuple_res[0]} {tuple_res[1]} discrete")
            else:
                print(f"{tuple_res[0]}  {tuple_res[1]}")
        return res

    except FileNotFoundError:
        exit("File not found.")


# Returns true if all vertexes do not have a unique coloring, otherwise false.
def not_unique(color: dict, graph_vertexes: list) -> bool:
    if len(color) == len(graph_vertexes):
        return False
    return True


# The color refinement algorithm itself, which shows a
def colorref(graph_inst: Graph):
    # Initialisation stage

    graph_vertexes = sorted(list(graph_inst.vertices), key=lambda v: v.label)
    color = {}

    # Extra step to round all vertexes not needed

    # initial_color = 1
    # for i in graph_vertexes:
    #     i.color = initial_color

    # Degree based coloring
    max_degree = -1
    for vertex in graph_vertexes:
        c = vertex.degree
        vertex.label = c
        if not color.get(c):
            color[c] = [vertex]
        else:
            color[c].append(vertex)
        max_degree = max(max_degree, c)
    color = {key: color[key] for key in sorted(color)}

    # The color refinement.
    changes = True
    iteration_counter = 0
    while not_unique(color, graph_vertexes) and changes:
        iteration_counter += 1
        changes = False
        new_color_assignments = {}
        # Choosing Which Vertex coloring to adjust
        for key, vertex_group in color.items():
            division = color_by_parts(vertex_group, max_degree)
            if len(division) > 1:
                changes = True
                new_color_assignments.update(division)
                for new_color, group in division.items():
                    for vertex in division.get(new_color):
                        vertex.label = new_color
                max_degree = max(max_degree, max(list(new_color_assignments.keys())))
        for updated_color, group in new_color_assignments.items():
            color[updated_color] = group
    return iteration_counter


# Divides the vertexes of the same color in a new color. Returns the dictionary of tuple and list of vertexes.
def color_by_parts(vertexes: list, max_degree: int) -> dict:
    if len(vertexes) == 1:
        return {vertexes[0].label: [vertexes[0]]}
    newest_color = max_degree + 1
    comparison = {}
    for vertex in vertexes:
        # Convert list to tuple to use as dictionary key
        neighbour_colors = tuple(get_neighbour_colors(vertex))
        if neighbour_colors in comparison:
            comparison[neighbour_colors].append(vertex)
        else:
            # Ensure the value is initialized as a list containing the vertex
            comparison[neighbour_colors] = [vertex]
    # Sorting based on the number of items changed
    # comparison = dict(sorted(comparison.items(), key=lambda item: len(item[1])))

    # Sorting based on the sum of neighbours
    comparison = dict(sorted(comparison.items(), key=lambda item: sum(item[0])))

    # Custom sorting
    comparison = dict(sorted(comparison.items(), key=custom_sort))
    res = {vertexes[0].label: comparison[list(comparison.keys())[0]]}
    # If coloring does not change
    if len(comparison.keys()) == 1:
        return res
    else:
        keys = list(comparison.keys())[1:]
        for key_group in keys:
            res[newest_color] = comparison[key_group]
            newest_color += 1  # Prepare the next label for the next group
    return res


# For a certain vertex returns a list of labels of the given vertex neighbours.
def get_neighbour_colors(vertex: Vertex) -> list:
    res = []
    for neighbour in vertex.neighbours:
        res.append(neighbour.label)
    return sorted(res)


def print_graph(g: Graph, name: str):
    for vertex in g.vertices:
        vertex.colornum = vertex.label
    with open('graph' + name + '.dot', 'w') as file:
        write_dot(g, file)


def get_all_colors(g: Graph) -> list:
    res = []
    for vertex in g.vertices:
        res.append(vertex.label)
    return sorted(res)


def are_perfectly_edged(edges: list, edges1: list):
    if len(edges) != len(edges1):
        return False
    else:
        dict_edges = edges_to_dict(edges)
        dict_edges2 = edges_to_dict(edges1)
        for key in dict_edges:
            if key not in dict_edges2:
                return False
            if dict_edges[key] != dict_edges2[key]:
                return False
    return True


def edges_to_dict(edges: list) -> dict:
    dict_edges = {}
    for edge in edges:
        if edge.head.label < edge.tail.label:
            edge_to_store = tuple([edge.head.label, edge.tail.label])
        else:
            edge_to_store = tuple([edge.tail.label, edge.head.label])

        if edge_to_store not in dict_edges:
            dict_edges[edge_to_store] = 1
        else:
            dict_edges[edge_to_store] = dict_edges[edge_to_store] + 1

    return dict_edges


def custom_sort(item):
    # Primary key: Sum of the tuple
    primary_key = sum(item[0])
    # Secondary key: The sorted tuple itself (this naturally prioritizes smaller numbers)
    secondary_key = sorted(item[0], reverse=True)  # Sort in reverse to prioritize smaller numbers at the end
    return (primary_key, secondary_key)


if __name__ == '__main__':
    test_list = ["colorref_largeexample_4_1026.grl",
                 "colorref_largeexample_6_960.grl",
                 "colorref_smallexample_2_49.grl",
                 "colorref_smallexample_4_16.grl",
                 "colorref_smallexample_4_7.grl",
                 "colorref_smallexample_6_15.grl",
                 "cref9vert3comp_10_27.grl",
                 "test_3reg.grl",
                 "test_cref9.grl",
                 "test_cycles.grl",
                 "test_empty.grl",
                 "test_iter.grl",
                 "test_trees.grl"]
    for file in test_list:
        print(file + "\n")

        print(basic_colorref(os.path.join("SampleGraphsBasicColorRefinement", file)))
        print("\n\n")

    # basic_colorref(os.path.join("SampleGraphsBasicColorRefinement", "cref9vert3comp_10_27.grl"))
