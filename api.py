import requests
import json
BASE_URL = "https://statusmatcher.com/api/"

def get_recent_reports(limit=999999,save=None):
    # Gets the `limit` most recent reports from the api
    # If `save` is not None, saves the reports to a file
    url = BASE_URL + f"report?page=0&size={limit}&view=recentReportList"
    response = requests.get(url)
    reports = response.json()
    if save is not None:
        with open(save, "w") as file:
            json.dump(reports, file)
    return reports

if __name__ == "__main__":
    reports = get_recent_reports(save="reports.json")
    print(reports)
