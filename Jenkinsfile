pipeline {
  agent any
  environment { APP_HOST = 'ubuntu@3.108.30.181' }

  stages {
    stage('Build') {
      steps { sh 'python3 -m py_compile */app.py' }
    }
    stage('Test') {
      steps { echo 'Syntax check passed' }
    }
    stage('Deploy') {
      steps {
        sshagent(['ec2-deploy-key']) {
          sh '''
            rsync -az --exclude .git -e "ssh -o StrictHostKeyChecking=no" ./ $APP_HOST:~/app/
            ssh $APP_HOST "bash ~/app/deploy.sh"
          '''
        }
      }
    }
  }
}