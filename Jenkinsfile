node {


   stage('Checkout Code') { 
      git 'https://github.com/maping/java-maven-calculator-web-app.git'
   }
   stage('JUnit Test') {
      if (isUnix()) {
         sh "mvn clean test"
      } else {
         bat(/"mvn" clean test/)
      }
   }
   stage('Integration Test') {
      if (isUnix()) {
         sh "'mvn' integration-test"
      } else {
         bat(/"mvn" integration-test/)
      }
   }
 /*
   stage('Performance Test') {
      if (isUnix()) {
         sh "'mvn' cargo:start verify cargo:stop"
      } else {
         bat(/"mvn" cargo:start verify cargo:stop/)
      }
   }
  */
  stage('Performance Test') {
      if (isUnix()) {
         sh "'mvn' verify"
      } else {
         bat(/"mvn" verify/)
      }
   }
   stage('Deploy') {
      timeout(time: 10, unit: 'MINUTES') {
           input message: 'Deploy this web app to production ?'
      }
      echo 'Deploy...'
   }
}
   
