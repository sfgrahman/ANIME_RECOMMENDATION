pipeline{
    agent any

    stages {
        stage("Cloning from Github..."){
            steps{
                script{
                    echo 'cloning from Github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/sfgrahman/ANIME_RECOMMENDATION.git']])
                }
            }
        }
    }
}