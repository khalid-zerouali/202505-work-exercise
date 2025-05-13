pipeline {
          agent any
          triggers { cron('0 1 * * *') }
          environment {
              OPENSEARCH_INITIAL_ADMIN_PASSWORD = 'ThisIsAdiPass1*'
              OPENSEARCH_HOST    = 'opensearch-node1'
          }
          stages {
            stage('Git Checkout') {
                steps {
                    script {
                        git branch: 'main',
                            url: 'https://github.com/khalid-zerouali/202505-work-exercise'
                    }
                }
            }
            stage('Install dependencies') {
              steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install "cython<3.0.0" wheel
                    pip install "pyyaml==5.4.1" --no-build-isolation
                    pip install -r /var/jenkins_home/requirements.txt
                '''
              }
            }
            stage('Schema validation') {
              steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    jsonschema -i monitors.json monitors_validator/monitors_schema-v1.0.0.json
                '''
              }
            }
            stage('Run OpenSearch Monitors Deployer') {
              steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python3 opensearch_ci/injector.py
                '''
              }
            }
            stage('Cleanup') {
              steps {
                echo 'Job done.'
              }
            }
          }
}