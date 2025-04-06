pipeline{
    agent any
    environment{
        VENV_DIR ='venv'
    }
    stages {
        stage("Cloning from Github..."){
            steps{
                script{
                    echo 'cloning from Github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/sfgrahman/ANIME_RECOMMENDATION.git']])
                }
            }
        }
   
    stage("Making a virtual environment ..."){
            steps{
                script{
                    echo 'Making a virtual environment..'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''
                    
                    }
            }
        }
         stage('DVC Pull') {
                steps {
                    script {
                        echo 'DVC Pull... using credentials from .dvc/config'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }

    
        
    }
}