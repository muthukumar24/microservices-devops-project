pipeline {
  agent any

  environment {
    APP_HOST = 'ubuntu@3.108.30.181'
    APP_IP   = '3.108.30.181'
  }

  stages {
    stage('Build') {
      steps {
        sh 'python3 -m py_compile user-service/app.py product-service/app.py order-service/app.py'
      }
    }

    stage('Test') {
      steps {
        sh 'echo "Syntax check passed"'
      }
    }

    stage('Deploy') {
      steps {
        sshagent(['ec2-ssh-key']) {
          sh '''
            rsync -az --delete --exclude .git -e "ssh -o StrictHostKeyChecking=no" ./ $APP_HOST:~/app/
            ssh -o StrictHostKeyChecking=no $APP_HOST '
              cd ~/app
              python3 -m venv venv
              venv/bin/pip install -q -r user-service/requirements.txt -r product-service/requirements.txt -r order-service/requirements.txt
              pm2 delete all || true
              pm2 start user-service/app.py       --name user-service    --interpreter $HOME/app/venv/bin/python
              pm2 start product-service/app.py --name product-service --interpreter $HOME/app/venv/bin/python
              pm2 start order-service/app.py     --name order-service   --interpreter $HOME/app/venv/bin/python
              pm2 save
            '
          '''
        }
      }
    }
  }
}