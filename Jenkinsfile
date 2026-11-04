
pipeline {

    agent any

    environment {
        APP_HOST = 'ubuntu@3.108.30.181'
        REMOTE_DIR = '/opt/microservices'
    }

    stages {

        // 1. Get application code from GitHub
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // 2. Install Python dependencies
        stage('Build') {
            steps {
                sh '''
                    echo "Building User Service"
                    cd user-service
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                    cd ..

                    echo "Building Product Service"
                    cd product-service
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                    cd ..

                    echo "Building Order Service"
                    cd order-service
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                    cd ..
                '''
            }
        }

        // 3. Test all three applications
        stage('Test') {
            steps {
                sh '''
                    echo "Testing User Service"
                    cd user-service
                    python3 -m compileall -q app.py
                    .venv/bin/python -c 'from app import app; response = app.test_client().get("/"); assert response.status_code == 200; print(response.get_data(as_text=True))'
                    cd ..

                    echo "Testing Product Service"
                    cd product-service
                    python3 -m compileall -q app.py
                    .venv/bin/python -c 'from app import app; response = app.test_client().get("/"); assert response.status_code == 200; print(response.get_data(as_text=True))'
                    cd ..

                    echo "Testing Order Service"
                    cd order-service
                    python3 -m compileall -q app.py
                    .venv/bin/python -c 'from app import app; response = app.test_client().get("/"); assert response.status_code == 200; print(response.get_data(as_text=True))'
                    cd ..
                '''
            }
        }

        // 4. Deploy applications to EC2
        stage('Deploy') {
            steps {

                sshagent(credentials: ['ec2-deploy-key']) {

                    sh '''
                        echo "Creating deployment directories on EC2"

                        ssh "$APP_HOST" "mkdir -p $REMOTE_DIR/user-service $REMOTE_DIR/product-service $REMOTE_DIR/order-service"

                        echo "Deploying User Service"
                        rsync -az --exclude='.venv' --exclude='__pycache__' user-service/ "$APP_HOST:$REMOTE_DIR/user-service/"

                        echo "Deploying Product Service"
                        rsync -az --exclude='.venv' --exclude='__pycache__' product-service/ "$APP_HOST:$REMOTE_DIR/product-service/"

                        echo "Deploying Order Service"
                        rsync -az --exclude='.venv' --exclude='__pycache__' order-service/ "$APP_HOST:$REMOTE_DIR/order-service/"

                        echo "Installing dependencies and restarting services"

                        ssh "$APP_HOST" "cd $REMOTE_DIR/user-service && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && sudo /usr/bin/systemctl restart user-service"

                        ssh "$APP_HOST" "cd $REMOTE_DIR/product-service && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && sudo /usr/bin/systemctl restart product-service"

                        ssh "$APP_HOST" "cd $REMOTE_DIR/order-service && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && sudo /usr/bin/systemctl restart order-service"

                        echo "Deployment completed"
                    '''
                }
            }
        }

        // 5. Verify that all services are running
        stage('Verify Deployment') {
            steps {
                sshagent(credentials: ['ec2-deploy-key']) {
                    sh '''
                        echo "Checking User Service"
                        ssh "$APP_HOST" "sudo /usr/bin/systemctl is-active user-service && curl -fsS http://localhost:5001/"

                        echo "Checking Product Service"
                        ssh "$APP_HOST" "sudo /usr/bin/systemctl is-active product-service && curl -fsS http://localhost:5002/"

                        echo "Checking Order Service"
                        ssh "$APP_HOST" "sudo /usr/bin/systemctl is-active order-service && curl -fsS http://localhost:5003/"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'All three microservices have been deployed and verified successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the Jenkins Console Output.'
        }
    }
}
