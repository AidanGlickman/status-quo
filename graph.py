from lib import *
from typing import List
import os
import itertools

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
    def __init__(self, statuses: List[Status], reports: List[Report]):
        self.nodes = {status.id: Node(status) for status in statuses}
        self.edges = {}
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
        return [EdgeSummary(edge) for edge in edges]

def read_graph_data(programs_path, reports_path) -> Graph:
    # programs = [read_program(programs_path + "/" + program) for program in os.listdir(programs_path)]
    programs = read_programs(programs_path)
    statuses = [status for program in programs for status in program.statuses]
    reports = [read_report(reports_path + "/" + report) for report in os.listdir(reports_path)]
    return Graph(statuses, reports)

if __name__ == "__main__":
    # HHonors Gold: 22696

    graph = read_graph_data("data/programs.json", "data/reports")
    summaries = graph.get_neighbors(22696)
    for summary in summaries:
        if(summary.counts[Result.MATCH] > 0):
            print(summary)
