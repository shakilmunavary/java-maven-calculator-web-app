**AI Powered Pre Git Push Validations**



🧠 Building an AI-Powered Code Review Pipeline with SonarCloud and Azure OpenAI
Modern software development demands more than just clean syntax—it requires secure, maintainable, and high-quality code. In this blog, I’ll walk you through how I built an intelligent code review pipeline that combines static analysis with AI-powered insights using SonarCloud, Azure OpenAI, and GitHub.

📌 Overview
This pipeline automatically reviews Java code during every push to GitHub. It compiles the project, runs a SonarCloud scan, and then uses Azure OpenAI to analyze both the changed Java files and the SonarCloud findings. The result? A smart, automated gatekeeper that blocks pushes if critical issues are found.

🧱 Architecture Diagram
Here’s a visual representation of the pipeline:
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/7ec4b16d-8dc9-40ab-95ca-8b9b29cdbac6" />


🔄 Workflow Breakdown
1. Git Push
The process begins when a developer pushes code to the GitHub repository.

2. Compile Java Project
Using Maven, the pipeline compiles the Java project to ensure there are no build-time errors.

3. Run SonarCloud Scan
SonarCloud performs static code analysis, checking for bugs, vulnerabilities, code smells, and test coverage.

4. Fetch Changed Java Files
The pipeline identifies which .java files were modified in the latest commit.

5. Fetch SonarCloud Findings
Unresolved issues from SonarCloud are retrieved using its public API.

6. Analyze with Azure OpenAI
Two AI reviews are performed:

Changed Java Files: Azure OpenAI analyzes the raw code for security flaws, bad practices, and quality issues.

SonarCloud Findings: The AI interprets the scan results and suggests remediations.

7. Display AI Recommendations
The pipeline prints two tables:

One for AI feedback on the changed Java files

One for AI feedback on SonarCloud findings

8. Push Decision
If any “High” severity issues are found, the push is blocked. Otherwise, it proceeds safely.

🧠 Why Use AI in Code Review?
Traditional static analysis tools are great at flagging issues—but they don’t explain them. By integrating Azure OpenAI, we get:

Context-aware recommendations

Human-like reasoning about code quality

Actionable insights for remediation

This makes the review process smarter, faster, and more developer-friendly.

🛠️ Technologies Used
Tool	Purpose
GitHub	Source control and trigger for pipeline
Maven	Java project compilation
SonarCloud	Static code analysis
Azure OpenAI	AI-powered code review and feedback
Python	Orchestration of the entire workflow
Rich	Beautiful CLI output with tables & panels
🚀 What’s Next?
This pipeline is just the beginning. You can extend it to:

Post AI feedback as GitHub PR comments

Auto-create GitHub issues for critical findings

Send alerts to Slack or Teams

Track historical trends in code quality

📚 Final Thoughts
By combining static analysis with AI, we’re not just catching bugs—we’re building smarter, more resilient software. This pipeline turns every push into a learning opportunity, helping developers write better code with every commit.

If you’d like to try this out or contribute, check out the GitHub repository.






# A Java Maven Calculator Web Application
A Java calculator web app, build by Maven, CI/CD by Jenkins.

![image](realworld-pipeline-flow.png)

## 1. Manualy Build, Test, and Deploy By Maven

### 1.1 Start Nexus (Optional)
```console
$ cd ~/sonatype/nexus/bin
$ ./nexus start 
```
Visit http://localhost:8081/ with admin/admin123.

### 1.2 Build
```console
$ mvn clean package -Dmaven.test.skip=true  
...
[INFO] Packaging webapp
[INFO] Assembling webapp [java-maven-calculator-web-app] in [/Users/maping/code/test/java-maven-calculator-web-app/target/calculator]
[INFO] Processing war project
[INFO] Copying webapp resources [/Users/maping/code/test/java-maven-calculator-web-app/src/main/webapp]
[INFO] Webapp assembled in [71 msecs]
[INFO] Building war: /Users/maping/code/test/java-maven-calculator-web-app/target/calculator.war
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  38.163 s
[INFO] Finished at: 2019-03-06T21:35:57+08:00
[INFO] ------------------------------------------------------------------------
```
>Explain: -DskipTests, not execute test case, but compile test case; -Dmaven.test.skip=true，not compile test case, neither execute test case.

>Attention: Due to China GFW, you may fail when you build this project. Try it outside China GFW.

### 1.3  Run Locally
```console
$ mvn jetty:run
[INFO] Scanning elapsed time=147ms
[INFO] DefaultSessionIdManager workerName=node0
[INFO] No SessionScavenger set, using defaults
[INFO] node0 Scavenging every 660000ms
[INFO] Started o.e.j.m.p.JettyWebAppContext@48535004{Calculator Web,/calculator,file:///Users/maping/code/java-maven-calculator-web-app/src/main/webapp/,AVAILABLE}{file:///Users/maping/code/java-maven-calculator-web-app/src/main/webapp/}
[INFO] Started ServerConnector@580fd26b{HTTP/1.1,[http/1.1]}{0.0.0.0:9999}
[INFO] Started @3779ms
[INFO] Started Jetty Server
```
By default, the jetty port is 9999, so you should visit following urls in browser:
- http://localhost:9999/calculator/api/calculator/ping
- http://localhost:9999/calculator/api/calculator/add?x=8&y=26
- http://localhost:9999/calculator/api/calculator/sub?x=12&y=8
- http://localhost:9999/calculator/api/calculator/mul?x=11&y=8
- http://localhost:9999/calculator/api/calculator/div?x=12&y=12

To run in a different port, `mvn jetty:run -Djetty.port=<Your-Port>`.

To debug locally, `set MAVEN_OPTS=-Xdebug -Xrunjdwp:transport=dt_socket,server=y,address=8000,suspend=n`, then `mvn jetty:run`.

To stop Jetty Server, press Control-C.

### 1.4 Run JUnit Test
```console
$ mvn clean test
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.qianhong.calculator.CalculatorServiceTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.051 s - in com.qianhong.calculator.CalculatorServiceTest
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
```
### 1.5 Run Integration Test
```console
$ mvn clean integration-test
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.qianhong.calculator.CalculatorServiceIT
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.782 s - in com.qianhong.calculator.CalculatorServiceIT
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
```
### 1.6 Deploy Your Web App to An Existed Tomcat 8x
Please install a Tomcat 8x on your machine, after that, you need change pom.xml, point to your own Tomcat 8x.
```console
$ mvn cargo:run
[INFO] [talledLocalContainer] 14-Mar-2019 10:10:19.495 信息 [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
[INFO] [talledLocalContainer] 14-Mar-2019 10:10:19.501 信息 [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["ajp-nio-8009"]
[INFO] [talledLocalContainer] 14-Mar-2019 10:10:19.503 信息 [main] org.apache.catalina.startup.Catalina.start Server startup in 2012 ms
[INFO] [talledLocalContainer] Tomcat 8.x started on port [8080]
[INFO] Press Ctrl-C to stop the container...
```
By default, the tomcat port is 8080, so you should visit following urls in browser:
- http://localhost:8080/calculator/api/calculator/ping
- http://localhost:8080/calculator/api/calculator/add?x=8&y=26
- http://localhost:8080/calculator/api/calculator/sub?x=12&y=8
- http://localhost:8080/calculator/api/calculator/mul?x=11&y=8
- http://localhost:8080/calculator/api/calculator/div?x=12&y=12

### 1.7 Run Performance Test with JMeter
>Important: make sure your Tomcat 8x is runing, before you run performance test.
```console
$ mvn clean verify
[INFO] -------------------------------------------------------
[INFO]  P E R F O R M A N C E    T E S T S
[INFO] -------------------------------------------------------
[INFO]  
[INFO]  
[INFO] Executing test: CalculatorTestPlan.jmx
[INFO] Starting process with:[java, -Xms512M, -Xmx512M, -jar, ApacheJMeter-4.0.jar, -d, /Users/maping/code/java-maven-calculator-web-app/target/jmeter, -e, -j, /Users/maping/code/java-maven-calculator-web-app/target/jmeter/logs/CalculatorTestPlan.jmx.log, -l, /Users/maping/code/java-maven-calculator-web-app/target/jmeter/results/20190314-CalculatorTestPlan.csv, -n, -o, /Users/maping/code/java-maven-calculator-web-app/target/jmeter/reports/CalculatorTestPlan_20190314_104015, -t, /Users/maping/code/java-maven-calculator-web-app/target/jmeter/testFiles/CalculatorTestPlan.jmx]
[INFO] Creating summariser <summary>
[INFO] Created the tree successfully using /Users/maping/code/java-maven-calculator-web-app/target/jmeter/testFiles/CalculatorTestPlan.jmx
[INFO] Starting the test @ Thu Mar 14 10:40:26 CST 2019 (1552531226967)
[INFO] Waiting for possible Shutdown/StopTestNow/Heapdump message on port 4445
[INFO] summary +     16 in 00:00:03 =    5.2/s Avg:    32 Min:     2 Max:   288 Err:     0 (0.00%) Active: 1 Started: 4 Finished: 3
[INFO] summary +     34 in 00:00:06 =    5.7/s Avg:     2 Min:     1 Max:     5 Err:     0 (0.00%) Active: 0 Started: 10 Finished: 10
[INFO] summary =     50 in 00:00:09 =    5.5/s Avg:    12 Min:     1 Max:   288 Err:     0 (0.00%)
[INFO] Tidying up ...    @ Thu Mar 14 10:40:36 CST 2019 (1552531236412)
[INFO] ... end of run
[INFO] Completed Test: /Users/maping/code/java-maven-calculator-web-app/target/jmeter/testFiles/CalculatorTestPlan.jmx
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  59.487 s
[INFO] Finished at: 2019-03-14T10:40:37+08:00
[INFO] ------------------------------------------------------------------------
[INFO] Shutdown detected, destroying JMeter process...
```
### 1.8 Start Jmeter GUI (Optional)
If you want to see the test plan, you need install Jmeter, then start Jmeter GUI and open java-maven-calculator-web-app/src/test/jmeter/CalculatorTestPlan.jmx.
```console
$ cd ~/apache/jmeter/bin
$ ./jmeter 
```
![image](jmeter-test-plan-02.png)

![image](jmeter-test-plan-02.png)

Don't use GUI mode for load testing !, only for Test creation and Test debugging.For load testing, use CLI Mode:
```console
$ cd ~/apache/jmeter/bin
$ ./jmeter.sh -n -t ~/code/java-maven-calculator-web-app/src/test/jmeter/CalculatorTestPlan.jmx -Jusers=20 -Jloop=2 -l ~/code/java-maven-calculator-web-app/src/test/jmeter/calculator_`date +'%y%m%d%H%M%S'`.csv
Creating summariser <summary>
Created the tree successfully using /Users/maping/code/java-maven-calculator-web-app/src/test/jmeter/CalculatorTestPlan.jmx
Starting the test @ Sat Mar 16 22:07:52 CST 2019 (1552745272072)
Waiting for possible Shutdown/StopTestNow/HeapDump/ThreadDump message on port 4445
summary +    161 in 00:00:08 =   19.9/s Avg:     1 Min:     1 Max:    52 Err:     0 (0.00%) Active: 1 Started: 17 Finished: 16
summary +     39 in 00:00:02 =   25.7/s Avg:     1 Min:     0 Max:     3 Err:     0 (0.00%) Active: 0 Started: 20 Finished: 20
summary =    200 in 00:00:10 =   20.8/s Avg:     1 Min:     0 Max:    52 Err:     0 (0.00%)
Tidying up ...    @ Sat Mar 16 22:08:01 CST 2019 (1552745281987)
```
Open performance test result csv file:
![image](jmeter-test-result-01.png)

### 1.9 Build Project Site
```console
$ mvn site
```
open java-maven-calculator-web-app/target/site/index.html
![image](mvn-site-01.png)

### 1.10 Deploy Artifactory to Nexus (Optional)
```console
$ mvn clean deploy
```

Visit http://localhost:8081/ with admin/admin123.

Search calculator, click Browse SNAPSHOT(s)

![image](nexus-browse-01.png)

### 1.11 Release X.0 version (Optional)
Before Release a version, you must commit and push all your code to remote repo.
```console
$ mvn release:prepare
...
[INFO] --- maven-release-plugin:2.5.3:prepare (default-cli) @ java-maven-calculator-web-app ---
[INFO] Resuming release from phase 'scm-check-modifications'
[INFO] Verifying that there are no local modifications...
[INFO]   ignoring changes on: **/pom.xml.releaseBackup, **/pom.xml.next, **/pom.xml.tag, **/pom.xml.branch, **/release.properties, **/pom.xml.backup
[INFO] Executing: /bin/sh -c cd /Users/maping/code/java-maven-calculator-web-app && git rev-parse --show-toplevel
[INFO] Working directory: /Users/maping/code/java-maven-calculator-web-app
[INFO] Executing: /bin/sh -c cd /Users/maping/code/java-maven-calculator-web-app && git status --porcelain .
[INFO] Working directory: /Users/maping/code/java-maven-calculator-web-app
[INFO] Checking dependencies and plugins for snapshots ...
What is the release version for "Calculator Web"? (com.qianhong.javawebapp:java-maven-calculator-web-app) 1.0: : 
What is SCM release tag or label for "Calculator Web"? (com.qianhong.javawebapp:java-maven-calculator-web-app) java-maven-calculator-web-app-1.0: : 
What is the new development version for "Calculator Web"? (com.qianhong.javawebapp:java-maven-calculator-web-app) 1.1-SNAPSHOT: : 
[INFO] Transforming 'Calculator Web'...
[INFO] Not generating release POMs
...
```
Now, release java-maven-calculator-web-app 1.0 to your Nexus. 
```console
$ mvn release:perform
...
[INFO] Uploaded to releases: http://localhost:8081/repository/maven-releases/com/qianhong/javawebapp/java-maven-calculator-web-app/1.0/java-maven-calculator-web-app-1.0-javadoc.jar (30 kB at 722 kB/s)
...
```

## 2. Automaticly Build, Test, and Deploy By Jenkins

### 2.1 Create and Configure a Freestyle Jenkins Project
Project name: **MyJavaMavenCalculateWebApp**

Execute every mvn goal one by one defined in Build Section Step: "Invoke top-level Maven targets"

![image](jenkins-mvn-01.png)

![image](jenkins-mvn-02.png)

### 2.2 Create and Configure a Pipeline Jenkins Project
Project name: **MyJavaMavenCalculateWebApp-Pipeline**

Execute the Jenkins Pipeline Script File: Jenkinsfile

![image](jenkins-pipeline-01.png)

![image](jenkins-pipeline-02.png)

### 2.3 Create and Configure a Freestyle Jenkins Project, using Publish Over FTP plugin
Project name: **MyJavaMavenCalculateWebApp-AzureAppService-FTP**

### 2.4 Create and Configure a Freestyle Jenkins Project, using Azure App Service plugin
Project name: **MyJavaMavenCalculateWebApp-AzureAppService**


## 3. Containerize Your Web App

### 3.1. Build a docker image using Dockerfile:
```console
$ docker build -t calculator .
Sending build context to Docker daemon  13.53MB
Step 1/4 : FROM tomcat
 ---> 48dd385504b1
Step 2/4 : MAINTAINER Ma Ping
 ---> Using cache
 ---> 3ae09eb166a2
Step 3/4 : RUN rm -rf $CATALINA_HOME/webapps/ROOT
 ---> Using cache
 ---> 20a183105b0e
Step 4/4 : COPY target/calculator.war $CATALINA_HOME/webapps/ROOT.war
 ---> 42b9363d582d
Successfully built 42b9363d582d
Successfully tagged calculator:latest
```

### 3.2. Run docker image locally
```console
$ docker run --rm -p 8181:8080 calculator
```
>Explain: --rm means delete the container after stopping it.

Access the web app at http://localhost:8181/api/calculator/ping in browser.

Press Control-C to stop and remove the container.

### 3.3. Push your local image to your docker hub repositories
```console
$ docker login -u <Your-Docker-ID> -p <Your-Docker-Password>
$ docker tag calculator <Your-Docker-ID>/calculator
$ docker push <Your-Docker-ID>/calculator
```

## 4. Deploy to Azure Web App using Container Image in Docker Hub
1. Create a Web App in Linux on Azure
2. Save the changes and you'll be able to access the web app in a few seconds.

## 5. Deploy to Your Azure Web App using Container Image in ACR
1. Create a Container Registry on Azure
2. Push your local image to ACR:
```
$ docker login <Your-ACR-Login-Server> -u <Your-ACR-Username> -p <Your-ACR-Password>
$ docker tag calculator <Your-ACR-Login-Server>/calculator
$ docker push <Your-ACR-Login-Server>/calculator
```
3. Create a Web App in Linux on Azure
4. In Docker Container settings of Web App, fill in image name, server URL, username and password of your ACR.
5. Save the changes and you'll be able to access the web app in a few seconds.

## Reference
- [Jenkins Pipeline](https://jenkins.io/doc/book/pipeline/)


