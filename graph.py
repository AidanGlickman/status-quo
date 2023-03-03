from lib import *
from typing import List
import os
import itertools
import pickle

class Node:
    def __init__(self, status: Status):
        self.status = status
        self.edges_from = {}

class Edge:
    def __init__(self, node_id_from, node_id_to):
        self.reports = {result: [] for result in Result}
        self.node_id_from = node_id_from
        self.node_id_to = node_id_to
    
    def add_report(self, report: Report):
        self.reports[report.result].append(report)

class EdgeSummary:
    def __init__(self, edge: Edge):
        self.edge = edge
        self.counts = {result: len(edge.reports[result]) for result in Result}
        self.pcts = {result: 0 if sum(self.counts.values()) == 0 else self.counts[result] / sum(self.counts.values()) for result in Result}

    def __str__(self):
        return f"EdgeSummary({self.edge.node_id_from} -> {self.edge.node_id_to}): {self.counts}"

class Graph:
    nodes = {}
    edges = {}
    programs = {}
    def __init__(self, statuses: List[Status], reports: List[Report], programs: List[Program]):
        self.nodes = {status.id: Node(status) for status in statuses}
        self.edges = {}
        self.programs = {program.id: program for program in programs}
        for fromstatus in statuses:
            for tostatus in statuses:
                if(fromstatus == tostatus):
                    continue
                if fromstatus.id not in self.edges:
                    self.edges[fromstatus.id] = {}
                self.edges[fromstatus.id][tostatus.id] = Edge(fromstatus.id, tostatus.id)

        for report in reports:
            # print(report.fromStatus, report.toStatus)
            if(report.fromStatus is None or report.toStatus is None):
                continue
            if(report.fromStatus not in self.edges or report.toStatus not in self.edges[report.fromStatus]):
                continue
            self.edges[report.fromStatus][report.toStatus].add_report(report)
            # print(report.fromStatus, report.toStatus, report.result)
        

    def get_neighbors(self, node_id):
        edges = list(filter(lambda x: len(x.reports) != 0, self.edges[node_id].values()))
        neighbors = [EdgeSummary(edge) for edge in edges]
        return neighbors
    
    def get_reach(self, node_id):
        # use BFS to find all nodes that can be reached from node_id where the edge has at least one report of a match
        # return a list of EdgeSummary objects
        seen = set()
        out = []
        queue = [node_id]
        while queue:
            node = queue.pop(0)
            if node not in seen:
                seen.add(node)
                for edge in self.edges[node].values():
                    if len(edge.reports[Result.MATCH]) > 0:
                        if edge.node_id_to not in seen:
                            queue.append(edge.node_id_to)
                            out.append(EdgeSummary(edge))
        return out
    

    def node_print_name(self, node_id):
        return f"{self.programs[self.nodes[node_id].status.program_id].name} {self.nodes[node_id].status.name}"

    def pretty_print_neighbors(self, node_id):
        print(f"Status Matches for Status {self.node_print_name(node_id)}")
        neighbors = self.get_neighbors(node_id)
        neighbors.sort(key=lambda x: x.counts[Result.MATCH], reverse=True)
        for summary in neighbors:
            if(summary.counts[Result.MATCH] > 0):
                print(f'\t{self.node_print_name(summary.edge.node_id_to)}: \n\t\tMatches: {summary.counts[Result.MATCH]} ({summary.pcts[Result.MATCH] * 100:.2f}%)\n\t\t Denies: {summary.counts[Result.DENY]} ({summary.pcts[Result.DENY] * 100:.2f}%)\n\t\t Challenges: {summary.counts[Result.CHALLENGE]} ({summary.pcts[Result.CHALLENGE] * 100:.2f}%) \n\t\t Others: {summary.counts[Result.OTHER]} ({summary.pcts[Result.OTHER] * 100:.2f}%)')

def read_graph_data(programs_path, reports_path, save_path=None) -> Graph:
    # programs = [read_program(programs_path + "/" + program) for program in os.listdir(programs_path)]
    programs = read_programs(programs_path)
    statuses = [status for program in programs for status in program.statuses]
    reports = [read_report(reports_path + "/" + report) for report in os.listdir(reports_path)]
    
    graph = Graph(statuses, reports, programs)
    if save_path is not None:
        # pickle and save
        with open(save_path, "wb") as f:
            pickle.dump(graph, f)
    return graph

def load_graph_data(path):
    with open(path, "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    # HHonors Gold: 22696

    # graph = read_graph_data("data/programs.json", "data/reports", "data/graph.pickle")
    graph = load_graph_data("data/graph.pickle")
    # graph.pretty_print_neighbors(22696)
    reach = graph.get_reach(52803)
    for edge in reach:
        print(f"{graph.node_print_name(edge.edge.node_id_from)} -> {graph.node_print_name(edge.edge.node_id_to)}: {edge.counts[Result.MATCH]}")
