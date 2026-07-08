def analyze_logs(file_path):

    with open(file_path, "r") as file:
        raw_logs = file.readlines()

    logs = []

    failed = 0
    critical = 0
    medium = 0
    low = 0

    incidents = []

    for index, line in enumerate(raw_logs, start=1):

        line = line.strip()

        severity = "LOW"

        status = "Closed"

        if "WARNING" in line:
            severity = "MEDIUM"
            status = "Investigating"
            failed += 1
            medium += 1

        elif "ERROR" in line:
            severity = "CRITICAL"
            status = "Open"
            critical += 1

        else:
            low += 1

        logs.append({
            "message": line,
            "severity": severity
        })

        if severity != "LOW":

            incidents.append({

                "id": index,
                "event": line,
                "severity": severity,
                "status": status

            })

    return {

        "logs": logs,
        "incidents": incidents,

        "failed": failed,

        "critical": critical,
        "medium": medium,
        "low": low,

        "total": len(logs),

        "alert": failed >= 5

    }