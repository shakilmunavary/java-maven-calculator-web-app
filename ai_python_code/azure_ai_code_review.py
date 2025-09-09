
import os
import subprocess
import requests
from openai import AzureOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

# Step 1: Load environment variables
console.print("[bold cyan]Step 1: Loading environment variables...[/bold cyan]")
load_dotenv()

required_vars = [
    "AZURE_API_KEY", "AZURE_API_BASE", "AZURE_API_VERSION", "AZURE_DEPLOYMENT_MODEL", "SONAR_TOKEN"
]
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    console.print(f"[red]❌ Missing environment variables: {', '.join(missing)}[/red]")
    exit(1)

# Step 2: Initialize Azure OpenAI
console.print("[bold cyan]Step 2: Initializing Azure OpenAI client...[/bold cyan]")
client = AzureOpenAI(
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_API_BASE")
)
deployment_name = os.getenv("AZURE_DEPLOYMENT_MODEL")
sonar_token = os.getenv("SONAR_TOKEN")

# Step 3: Compile Java and run SonarCloud scan
def run_sonar_scan():
    console.print("[bold cyan]Step 3: Compiling Java project with Maven...[/bold cyan]")
    compile_result = subprocess.run(["mvn", "clean", "compile"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if compile_result.returncode != 0:
        console.print("[red]❌ Maven compilation failed.[/red]")
        console.print(Panel(compile_result.stderr, title="Maven Error", style="red"))
        return False
    console.print("[green]✅ Maven compilation successful.[/green]")

    console.print("[bold cyan]Step 4: Running SonarCloud scan...[/bold cyan]")
    scan_cmd = [
        "sonar-scanner",
        "-Dsonar.organization=ai-test-code-quality",
        "-Dsonar.projectKey=ai-test-code-quality_ai-codereview",
        "-Dsonar.host.url=https://sonarcloud.io",
        f"-Dsonar.login={sonar_token}",
        "-Dsonar.java.binaries=target/classes",
        "-Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml"
    ]
    scan_result = subprocess.run(scan_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if scan_result.returncode != 0:
        console.print("[red]❌ SonarCloud scan failed.[/red]")
        console.print(Panel(scan_result.stderr, title="SonarCloud Error", style="red"))
        return False
    console.print("[green]✅ SonarCloud scan completed.[/green]")
    return True

# Step 4: Get committed Java files
def get_recently_committed_java_files():
    console.print("[bold cyan]Step 5: Fetching changed Java files from last commit...[/bold cyan]")
    result = subprocess.run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    files = result.stdout.strip().split("\n")
    java_files = [f for f in files if f.endswith(".java")]
    console.print(f"[green]✅ Found {len(java_files)} changed Java file(s):[/green] {', '.join(java_files)}")
    return java_files

# Step 5: Read file content
def read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"

# Step 6: Analyze code or findings with Azure OpenAI
def analyze_code_with_ai(file_name, code, is_sonar=False):
    if is_sonar:
        prompt = f"""
You are a secure code reviewer. Analyze the following SonarCloud issue summary and provide:
- A categorized breakdown of issues (bugs, vulnerabilities, code smells)
- Suggested remediations
- Highlight any critical risks

Return your findings as a list of recommendations in this format:
[("Issue Type", "Description", "Severity")]

SonarCloud Findings:
{code}
"""
    else:
        prompt = f"""
You are a secure code reviewer. Analyze the following Java code for:
- Code quality issues
- Security vulnerabilities
- Best practices violations

Return your findings as a list of recommendations in this format:
[("Issue Type", "Description", "Severity")]

If you find any critical issues, use severity "High". Otherwise use "Medium" or "Low".

File: {file_name}
Code:
{code}
"""

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a senior software engineer and security auditor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        content = response.choices[0].message.content
        if content.strip().startswith("["):
            return eval(content.strip())
        else:
            return [("AI Output", content.strip(), "Info")]
    except Exception as e:
        return [("Parsing Error", str(e), "High")]
# Step 7: Fetch SonarCloud issues
def fetch_sonar_issues():
    console.print("[bold cyan]Step 6: Fetching SonarCloud issues via API...[/bold cyan]")
    url = "https://sonarcloud.io/api/issues/search"
    params = {
        "componentKeys": "ai-test-code-quality_ai-codereview",
        "resolved": "false"
    }
    try:
        response = requests.get(url, params=params, auth=(sonar_token, ""))
        data = response.json()
        issues = data.get("issues", [])
        summary = "\n".join([f"- {i['severity']}: {i['message']} ({i['component']})" for i in issues])
        console.print(f"[green]✅ Retrieved {len(issues)} issue(s) from SonarCloud.[/green]")
        return summary if summary else "No unresolved issues found."
    except Exception as e:
        return f"Error fetching SonarCloud issues: {str(e)}"

# Step 8: Main workflow
def main():
    console.print("[bold yellow]🔍 Running Azure AI code review...[/bold yellow]")

    if not run_sonar_scan():
        console.print("[red]🛑 Workflow terminated due to SonarCloud scan failure.[/red]")
        exit(1)

    java_files = get_recently_committed_java_files()
    java_recommendations = []
    critical_found = False

    console.print("[bold cyan]Step 5: Reviewing changed Java files with AI...[/bold cyan]")
    for file_path in java_files:
        code = read_file_content(file_path)
        recommendations = analyze_code_with_ai(file_path, code)
        java_recommendations.extend(recommendations)
        for _, _, severity in recommendations:
            if severity.strip().lower() == "high":
                critical_found = True

    if java_recommendations:
        table = Table(title="🧠 AI Recommendations from Java Code", box=box.SIMPLE_HEAVY)
        table.add_column("Issue Type", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Severity", style="red")
        for issue_type, description, severity in java_recommendations:
            table.add_row(issue_type, description, severity)
        console.print(table)
    else:
        console.print("[green]✅ No AI recommendations found in Java files.[/green]")

    sonar_findings = fetch_sonar_issues()
    console.print("[bold cyan]Step 7: Reviewing SonarCloud findings with AI...[/bold cyan]")
    sonar_recommendations = analyze_code_with_ai("SonarCloud Findings", sonar_findings, is_sonar=True)

    if sonar_recommendations:
        sonar_table = Table(title="🧠 AI Recommendations from SonarCloud Findings", box=box.SIMPLE_HEAVY)
        sonar_table.add_column("Issue Type", style="cyan", no_wrap=True)
        sonar_table.add_column("Description", style="white")
        sonar_table.add_column("Severity", style="red")
        for issue_type, description, severity in sonar_recommendations:
            sonar_table.add_row(issue_type, description, severity)
            if severity.strip().lower() == "high":
                critical_found = True
        console.print(sonar_table)
    else:
        console.print("[green]✅ No critical AI recommendations from SonarCloud findings.[/green]")

    dashboard_url = "https://sonarcloud.io/summary/new_code?id=ai-test-code-quality_ai-codereview&branch=master"
    console.print(f"\n[bold blue]🔗 View full SonarCloud report:[/bold blue] [underline]{dashboard_url}[/underline]")

    if critical_found:
        console.print("[bold red]❌ Critical issues found in code. Blocking push.[/bold red]")
        exit(1)

    console.print("[bold green]✅ All checks passed. Safe to push.[/bold green]")
    exit(0)

if __name__ == "__main__":
    main()
