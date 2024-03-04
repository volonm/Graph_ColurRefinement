import datetime
import os

import graph
from graph import Graph, Vertex
from graph_io import load_graph, write_dot


def basic_colorref(path):
    try:
        with open(path) as f:
            G, properties = load_graph(f, Graph, read_list=True)

        graph_dict = {}

        for index, file_graph in enumerate(G):
            print_graph(file_graph, f"{index}_BEFORE")
            colorref(file_graph)
            graph_dict[index] = file_graph
            print_graph(file_graph, f"{index}_AFTER")


        # if not os.path.exists("graphs"):
        #     os.makedirs("graphs")
        #
        # # Somehow import graph
        # for file_graph in G:
        #     time = f"uniqueId + {datetime.datetime.now().strftime('%Y%m%d%H%M')}"
        #     print_graph(file_graph, f"{time}_BEFORE")
        #     colorref(file_graph)
        #     print_graph(file_graph, os.path.join("graphs", f"{time}_AFTER"))

    except FileNotFoundError:
        exit("File not found.")


# Returns true if all vertexes do not have a unique coloring, otherwise false.
def not_unique(color: dict, graph_vertexes: list) -> bool:
    if len(color) == len(graph_vertexes):
        return False
    return True


def colorref(graph_inst: Graph):
    # Initialisation stage

    graph_vertexes = sorted(list(graph_inst.vertices), key=lambda v: v.label)
    color = {}

    # Extra step to round all vertexes
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

    changes = True
    while not_unique(color, graph_vertexes) and changes:
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
            # keys_to_adjust = list(division.keys())
            #     # color[key] = division[keys_to_adjust[0]]
            # for key_to_new_group in keys_to_adjust[1:]:
            #     new_color = max(color.keys()) + 1
            #     color[new_color] = division[key_to_new_group]
            #     for vertex in division[key_to_new_group]:
            #         vertex.label = new_color

        # Adjusting the colors
    print("Graph vertexes:", color)
    # graphs = G[0]
    # print(graphs)
    # print(G[0][0])
    #
    # vert = graph_inst.vertices[0]
    # vert.color = 'red'


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


if __name__ == '__main__':
    basic_colorref("SampleGraphsBasicColorRefinement/colorref_smallexample_4_7.grl")
