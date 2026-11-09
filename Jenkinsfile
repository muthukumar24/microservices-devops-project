pipeline {
  agent any

  environment {
    APP_HOST = 'ubuntu@13.233.160.169'
    APP_IP   = '13.233.160.169'
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
            rsync -az --delete --exclude .git --exclude venv \
            -e "ssh -o StrictHostKeyChecking=no" \
            ./ $APP_HOST:~/app/

            ssh -o StrictHostKeyChecking=no $APP_HOST '
              cd ~/app

              python3 -m venv venv

              # Install dependencies
              venv/bin/pip install -q \
                -r user-service/requirements.txt \
                -r product-service/requirements.txt \
                -r order-service/requirements.txt

              # Restart User Service if it exists; otherwise start it
              pm2 describe user-service >/dev/null 2>&1 && \
              pm2 restart user-service || \
              pm2 start user-service/app.py \
                --name user-service \
                --interpreter $HOME/app/venv/bin/python

              # Restart Product Service
              pm2 describe product-service >/dev/null 2>&1 && \
              pm2 restart product-service || \
              pm2 start product-service/app.py \
                --name product-service \
                --interpreter $HOME/app/venv/bin/python

              # Restart Order Service
              pm2 describe order-service >/dev/null 2>&1 && \
              pm2 restart order-service || \
              pm2 start order-service/app.py \
                --name order-service \
                --interpreter $HOME/app/venv/bin/python

              # Save PM2 processes
              pm2 save

              # Display process status
              pm2 status
              '
          '''
        }
      }
    }
  }
}