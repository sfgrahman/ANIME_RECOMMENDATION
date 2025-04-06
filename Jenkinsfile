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

    
        stage('Build and Push Image to DockerHub') {
                steps {
                    withCredentials([usernamePassword(credentialsId: 'jenkins-test',
                                                    usernameVariable: 'DOCKERHUB_USERNAME',
                                                    passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                        script {
                            echo 'Build and Push Image to Docker Hub'

                            sh '''
                            echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

                            docker build -t $DOCKERHUB_USERNAME/anime-recommendation:latest .

                            docker push $DOCKERHUB_USERNAME/anime-recommendation:latest

                            docker logout
                            '''
                        }
                    }
                }
            }


        stage('Deploying to Kubernetes'){
            steps{
                withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
                    script{
                        echo 'Deploying to Kubernetes'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials ml-app-cluster --region us-central1
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        
        }
    }
}