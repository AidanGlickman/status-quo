from typing import List
from enum import Enum
import json

class Industry(Enum):
    HOTEL = "HOTEL"
    AUTO = "AUTO"
    AIRLINES = "AIRLINES"

class Result(Enum):
    MATCH = "MATCH"
    DENY = "DENY"
    CHALLENGE = "CHALLENGE"
    OTHER = "OTHER"

class Company:
    def __init__(self, id: int, name: str, alias: str, active: bool):
        self.id = id
        self.name = name
        self.alias = alias
        self.active = active
    
    def __str__(self):
        return f"Company(id={self.id}, name={self.name}, alias={self.alias}, active={self.active})"

class Status:
    def __init__(self, id: int, name: str, program_id: int, level: int, color: str):
        self.id = id
        self.name = name
        self.program_id = program_id
        self.level = level
        self.color = color
    
    def __str__(self):
        return f"Status(id={self.id}, name={self.name}, program_id={self.program_id}, level={self.level}, color={self.color})"

class Program:
    def __init__(self, id: int, name: str, industry: Industry, url: str, email: str, companies: List[Company], statuses: List):
        self.id = id
        self.name = name
        self.industry = industry
        self.url = url
        self.email = email
        self.companies = companies
        self.statuses = statuses
    
    def __str__(self):
        return f"Program(id={self.id}, name={self.name}, industry={self.industry}, url={self.url}, email={self.email}, companies=[{', '.join(str(company) for company in self.companies)}], statuses=[{', '.join(str(status) for status in self.statuses)}])"

class Report:
    def __init__(self, id: int, instructions: str, result: Result, published: bool, read: bool, fromStatusId, toStatusId):
        self.id = id
        self.instructions = instructions
        self.result = result
        self.published = published
        self.read = read
        self.fromStatus = fromStatusId
        self.toStatus = toStatusId
    
    def __str__(self):
        return f"Report(id={self.id}, instructions={self.instructions}, result={self.result}, published={self.published}, read={self.read}, fromStatus={self.fromStatus}, toStatus={self.toStatus})"

def read_program(path: str) -> Program:
    # read an independent program file
    with open(path, "r") as f:
        data = json.load(f)
        return Program(
            data["id"],
            data["name"],
            Industry(data["industry"]),
            data["url"],
            data["email"],
            [Company(c['id'], c['name'], c['alias'], c['active']) for c in data["companies"]],
            [Status(s['id'], s['name'], data['id'], s['level'], s['color']) for s in data["statuses"]]
        )

def read_programs(path: str) -> List[Program]:
    # read the combined programs file
    with open(path, "r") as f:
        data = json.load(f)
        return [Program(
            program["id"],
            program["name"],
            None,
            None,
            None,
            None,
            # Industry(program["industry"]),
            # program["url"],
            # program["email"],
            # [Company(c['id'], c['name'], c['alias'], c['active']) for c in program["companies"]],
            [Status(s['id'], s['name'], program['id'], s['level'], s['color']) for s in program["statuses"]]
        ) for program in data]

def read_report(path: str) -> Report:
    with open(path, "r") as f:
        data = json.load(f)
        return Report(
            data["id"],
            data["instructions"],
            Result(data["result"]),
            data["published"],
            data["read"],
            data["fromStatusId"],
            data["toStatusId"]
        )

if __name__ == "__main__":
    program = read_program("data/programs/21152.json")
    print(program)

    report = read_report("data/reports/84118.json")
    print(report)
