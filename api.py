import requests
import json
BASE_URL = "https://statusmatcher.com/api/"

def get_recent_reports(limit=8,save=None):
    # Gets the `limit` most recent reports from the api
    # If `save` is not None, saves the reports to a file
    # Set limit to 0 to get all reports
    if limit == 0:
        limit = 9999999
    url = BASE_URL + f"report?page=0&size={limit}&view=recentReportList"
    response = requests.get(url)
    reports = response.json()
    if save is not None:
        with open(save, "w") as file:
            json.dump(reports, file)
    return reports

def get_report(report_id,save=None):
    # Gets the report with the given id
    # If `save` is not None, saves the report to a file
    url = BASE_URL + f"report/{report_id}?view=full"
    response = requests.get(url)
    report = response.json()
    if save is not None:
        with open(save, "w") as file:
            json.dump(report, file)
    return report

def get_programs_and_statuses(save=None):
    # Gets all programs and their statuses
    # If `save` is not None, saves the report to a file
    url = BASE_URL + "program?view=programAndStatuses"
    response = requests.get(url)
    programs = response.json()
    if save is not None:
        with open(save, "w") as file:
            json.dump(programs, file)
    return programs

if __name__ == "__main__":
    programs = get_programs_and_statuses(save="programs.json")
