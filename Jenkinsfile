
pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t week12-registration .'
            }
        }

        stage('Deploy Container') {
            steps {
                bat 'docker rm -f week12-registration-container >nul 2>&1'
                bat 'docker run -d -p 5001:5000 --name week12-registration-container week12-registration'
            }
        }

        stage('Wait for Application') {
            steps {
                powershell '''
                    $ready = $false

                    for ($i = 0; $i -lt 30; $i++) {
                        try {
                            $response = Invoke-WebRequest `
                                -Uri "http://localhost:5001" `
                                -UseBasicParsing -TimeoutSec 2

                            if ($response.StatusCode -eq 200) {
                                $ready = $true
                                break
                            }
                        } catch {}

                        Start-Sleep -Seconds 2
                    }

                    if (-not $ready) {
                        docker logs week12-registration-container
                        exit 1
                    }
                '''
            }
        }

        stage('Selenium Testing') {
            steps {
                bat 'python -m pytest tests/test_registration.py -v --junitxml=test-results.xml'
            }
        }
    }

    post {
        always {
            junit testResults: 'test-results.xml',
                  allowEmptyResults: true

            bat 'docker rm -f week12-registration-container >nul 2>&1'
        }
    }
}
