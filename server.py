"""
SentinelScan Cloud MCP Server

A remote Model Context Protocol (MCP) server that exposes hardcoded
application security testing data (applications, scans, issues) so that
LLM-based clients can query security posture using natural language.

This server is inspired by HCL AppScan on Cloud's MCP server but all
responses are hardcoded mock data for demonstration purposes.

Transport: Streamable HTTP on the /mcp endpoint.
"""

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Server metadata
# ---------------------------------------------------------------------------

SERVER_NAME = "SentinelScan Cloud MCP Server"
SERVER_VERSION = "1.0.0"

mcp = FastMCP(
    name=SERVER_NAME,
    instructions=(
        "SentinelScan Cloud MCP Server exposes hardcoded application security "
        "testing data. Use the provided tools to list applications, inspect "
        "scans, and triage issues across SAST, DAST, SCA, and IAST findings."
    ),
    host="0.0.0.0",
    port=8000,
)

# ---------------------------------------------------------------------------
# Hardcoded mock dataset
# ---------------------------------------------------------------------------

APPLICATIONS = [
    {
        "id": "app-1001",
        "name": "Online Banking Portal",
        "business_unit": "Retail Banking",
        "risk_rating": "High",
        "technologies": ["Java", "Spring Boot", "React"],
        "last_scan_date": "2026-04-05T10:15:00Z",
        "total_issues": 42,
        "critical_issues": 3,
        "high_issues": 8,
        "medium_issues": 19,
        "low_issues": 12,
    },
    {
        "id": "app-1002",
        "name": "Customer Mobile App",
        "business_unit": "Mobile Engineering",
        "risk_rating": "Medium",
        "technologies": ["Kotlin", "Swift", "Node.js"],
        "last_scan_date": "2026-04-06T14:30:00Z",
        "total_issues": 17,
        "critical_issues": 0,
        "high_issues": 2,
        "medium_issues": 9,
        "low_issues": 6,
    },
    {
        "id": "app-1003",
        "name": "Internal HR System",
        "business_unit": "Human Resources",
        "risk_rating": "Low",
        "technologies": ["Python", "Django", "PostgreSQL"],
        "last_scan_date": "2026-04-02T08:45:00Z",
        "total_issues": 5,
        "critical_issues": 0,
        "high_issues": 0,
        "medium_issues": 2,
        "low_issues": 3,
    },
]

SCANS = [
    {
        "id": "scan-5001",
        "application_id": "app-1001",
        "name": "Banking Portal - Weekly SAST",
        "technology": "SAST",
        "status": "Completed",
        "started_at": "2026-04-05T09:00:00Z",
        "completed_at": "2026-04-05T10:15:00Z",
        "total_issues": 30,
    },
    {
        "id": "scan-5002",
        "application_id": "app-1001",
        "name": "Banking Portal - Production DAST",
        "technology": "DAST",
        "status": "Completed",
        "started_at": "2026-04-04T22:00:00Z",
        "completed_at": "2026-04-05T02:10:00Z",
        "total_issues": 12,
    },
    {
        "id": "scan-5003",
        "application_id": "app-1002",
        "name": "Mobile App - SCA Dependency Scan",
        "technology": "SCA",
        "status": "Completed",
        "started_at": "2026-04-06T14:00:00Z",
        "completed_at": "2026-04-06T14:30:00Z",
        "total_issues": 17,
    },
    {
        "id": "scan-5004",
        "application_id": "app-1003",
        "name": "HR System - Nightly IAST",
        "technology": "IAST",
        "status": "Completed",
        "started_at": "2026-04-02T03:00:00Z",
        "completed_at": "2026-04-02T08:45:00Z",
        "total_issues": 5,
    },
]

ISSUES = [
    {
        "id": "issue-9001",
        "application_id": "app-1001",
        "scan_id": "scan-5001",
        "title": "SQL Injection in LoginController",
        "severity": "Critical",
        "status": "Open",
        "cwe": "CWE-89",
        "technology": "SAST",
        "file": "src/main/java/com/bank/controller/LoginController.java",
        "line": 142,
        "trace": [
            "HttpServletRequest.getParameter(\"username\") at LoginController.java:138",
            "UserRepository.findByUsername(String) at UserRepository.java:57",
            "java.sql.Statement.executeQuery(String) at UserRepository.java:62",
        ],
        "remediation": (
            "Use PreparedStatement with parameterized queries instead of "
            "concatenating user input into raw SQL. Validate and sanitize all "
            "inputs originating from HTTP request parameters."
        ),
    },
    {
        "id": "issue-9002",
        "application_id": "app-1001",
        "scan_id": "scan-5001",
        "title": "Cross-Site Scripting (Reflected) on /search",
        "severity": "High",
        "status": "Open",
        "cwe": "CWE-79",
        "technology": "SAST",
        "file": "src/main/webapp/WEB-INF/views/search.jsp",
        "line": 24,
        "trace": [
            "HttpServletRequest.getParameter(\"q\") at SearchController.java:45",
            "Model.addAttribute(\"query\", String) at SearchController.java:46",
            "JSP expression ${query} at search.jsp:24",
        ],
        "remediation": (
            "Encode output using JSTL <c:out> or a context-aware escaping "
            "library before rendering user-controlled data into HTML."
        ),
    },
    {
        "id": "issue-9003",
        "application_id": "app-1001",
        "scan_id": "scan-5002",
        "title": "Missing HTTP Strict-Transport-Security header",
        "severity": "Medium",
        "status": "Open",
        "cwe": "CWE-319",
        "technology": "DAST",
        "file": "N/A",
        "line": 0,
        "trace": [
            "GET https://banking.example.com/ - response missing HSTS header",
        ],
        "remediation": (
            "Configure the web server or reverse proxy to emit "
            "'Strict-Transport-Security: max-age=31536000; includeSubDomains' "
            "on all HTTPS responses."
        ),
    },
    {
        "id": "issue-9004",
        "application_id": "app-1002",
        "scan_id": "scan-5003",
        "title": "Vulnerable dependency: lodash 4.17.11",
        "severity": "High",
        "status": "Open",
        "cwe": "CWE-1035",
        "technology": "SCA",
        "file": "package-lock.json",
        "line": 0,
        "trace": [
            "package.json declares lodash ^4.17.11",
            "Transitive usage via express-validator@6.4.0",
        ],
        "remediation": (
            "Upgrade lodash to >= 4.17.21 to address CVE-2020-8203 and "
            "CVE-2021-23337. Run 'npm audit fix' and retest."
        ),
    },
    {
        "id": "issue-9005",
        "application_id": "app-1003",
        "scan_id": "scan-5004",
        "title": "Insecure deserialization in report export",
        "severity": "Medium",
        "status": "Fixed",
        "cwe": "CWE-502",
        "technology": "IAST",
        "file": "hr_system/reports/export.py",
        "line": 88,
        "trace": [
            "pickle.loads(request.body) at export.py:88",
        ],
        "remediation": (
            "Replace pickle with a safe serialization format such as JSON, "
            "and validate the schema of incoming payloads."
        ),
    },
]

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def get_applications() -> dict:
    """List all applications onboarded to SentinelScan Cloud.

    Returns a hardcoded collection of application records, including
    risk rating, technology stack, and issue counts per severity.
    """
    return {
        "server": SERVER_NAME,
        "count": len(APPLICATIONS),
        "applications": APPLICATIONS,
    }


@mcp.tool()
def get_application_details(application_id: str) -> dict:
    """Get detailed information about a single application by its ID.

    Args:
        application_id: The SentinelScan application identifier (e.g. "app-1001").
    """
    for app in APPLICATIONS:
        if app["id"] == application_id:
            return {"server": SERVER_NAME, "application": app}
    return {
        "server": SERVER_NAME,
        "error": f"Application '{application_id}' not found",
    }


@mcp.tool()
def get_scans(application_id: str = "") -> dict:
    """List scans, optionally filtered by application.

    Args:
        application_id: Optional application ID to filter scans. If empty,
            returns all scans across every application.
    """
    if application_id:
        filtered = [s for s in SCANS if s["application_id"] == application_id]
    else:
        filtered = SCANS
    return {
        "server": SERVER_NAME,
        "count": len(filtered),
        "scans": filtered,
    }


@mcp.tool()
def get_scan_details(scan_id: str) -> dict:
    """Get detailed information about a single scan execution.

    Args:
        scan_id: The SentinelScan scan identifier (e.g. "scan-5001").
    """
    for scan in SCANS:
        if scan["id"] == scan_id:
            return {"server": SERVER_NAME, "scan": scan}
    return {"server": SERVER_NAME, "error": f"Scan '{scan_id}' not found"}


@mcp.tool()
def get_issues(
    application_id: str = "",
    scan_id: str = "",
    severity: str = "",
    status: str = "",
) -> dict:
    """Query security issues, filterable by application, scan, severity, or status.

    Args:
        application_id: Optional application ID filter (e.g. "app-1001").
        scan_id: Optional scan ID filter (e.g. "scan-5001").
        severity: Optional severity filter - one of "Critical", "High",
            "Medium", "Low", "Informational".
        status: Optional status filter - one of "Open", "Fixed", "Reopened",
            "In Review".
    """
    results = ISSUES
    if application_id:
        results = [i for i in results if i["application_id"] == application_id]
    if scan_id:
        results = [i for i in results if i["scan_id"] == scan_id]
    if severity:
        results = [i for i in results if i["severity"].lower() == severity.lower()]
    if status:
        results = [i for i in results if i["status"].lower() == status.lower()]

    summary = [
        {
            "id": i["id"],
            "title": i["title"],
            "severity": i["severity"],
            "status": i["status"],
            "technology": i["technology"],
        }
        for i in results
    ]
    return {
        "server": SERVER_NAME,
        "count": len(summary),
        "issues": summary,
    }


@mcp.tool()
def get_issue_details(issue_id: str) -> dict:
    """Retrieve full details for a specific security issue.

    Provides the file location, vulnerability trace, CWE classification,
    and concrete remediation guidance for the given issue.

    Args:
        issue_id: The SentinelScan issue identifier (e.g. "issue-9001").
    """
    for issue in ISSUES:
        if issue["id"] == issue_id:
            return {"server": SERVER_NAME, "issue": issue}
    return {"server": SERVER_NAME, "error": f"Issue '{issue_id}' not found"}


@mcp.tool()
def get_dashboard_summary() -> dict:
    """Return an overall SentinelScan Cloud security posture summary.

    Aggregates hardcoded counts across all applications and scans.
    """
    total_apps = len(APPLICATIONS)
    total_scans = len(SCANS)
    total_issues = len(ISSUES)
    by_severity = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for issue in ISSUES:
        by_severity[issue["severity"]] = by_severity.get(issue["severity"], 0) + 1
    return {
        "server": SERVER_NAME,
        "version": SERVER_VERSION,
        "total_applications": total_apps,
        "total_scans": total_scans,
        "total_issues": total_issues,
        "issues_by_severity": by_severity,
    }


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------


@mcp.prompt()
def sentinelscan_doc() -> str:
    """Load SentinelScan Cloud usage rules and schema into the model context."""
    return (
        "You are connected to the SentinelScan Cloud MCP Server.\n\n"
        "Available tools:\n"
        "  - get_applications(): list all applications.\n"
        "  - get_application_details(application_id): details for one app.\n"
        "  - get_scans(application_id?): list scans, optionally by app.\n"
        "  - get_scan_details(scan_id): details for one scan execution.\n"
        "  - get_issues(application_id?, scan_id?, severity?, status?): "
        "filter issues.\n"
        "  - get_issue_details(issue_id): full issue info with remediation.\n"
        "  - get_dashboard_summary(): overall posture summary.\n\n"
        "ID conventions:\n"
        "  - Application IDs look like 'app-1001'.\n"
        "  - Scan IDs look like 'scan-5001'.\n"
        "  - Issue IDs look like 'issue-9001'.\n\n"
        "Severities: Critical, High, Medium, Low, Informational.\n"
        "Statuses:   Open, Fixed, Reopened, In Review.\n"
        "Technologies: SAST, DAST, SCA, IAST.\n\n"
        "All data returned by this server is hardcoded mock data intended "
        "for demonstration and testing only."
    )


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Run as a remote MCP server over Streamable HTTP on /mcp
    mcp.run(transport="streamable-http")
