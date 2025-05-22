pipeline {
    agent any

    environment {
        REGISTRY = "harbor-uqi.boer.id/ci-cd"
        IMAGE_NAME = "flask-crud"
        IMAGE_TAG = "${BUILD_NUMBER}"
        MANIFEST_REPO = "https://github.com/luqinthar/flask-crud.git"
    }

    stages {
        stage('Build and Push Docker Image') {
            steps {
                git branch: 'main', url: 'https://github.com/luqinthar/flask-crud.git', credentialsId: 'github'
                script {
                    docker.withRegistry("http://${REGISTRY}", "jenkins-harbor") {
                        def image = docker.build("${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}-${BRANCH_NAME}")
                        image.push()
                    }
                }
            }
        }

        stage('Update Kustomization Image') {
            steps {
                dir('manifest') {
                    git branch: 'main', url: '${MANIFEST_REPO}', credentialsId: 'github'

                    script {
                        def kustomizationFile = "overlays/${BRANCH_NAME}/kustomization.yaml"
                        sh """
                        ls -l
                        echo "Updating image in ${kustomizationFile}"
                        sed -i "s|newName:.*|newName: ${REGISTRY}/${IMAGE_NAME}|" ${kustomizationFile}
                        sed -i "s|newTag:.*|newTag: ${IMAGE_TAG}|" ${kustomizationFile}

                        git config user.email "jenkins-uqi@keyz.my.id"
                        git config user.name "Jenkins CI"
                        git add ${kustomizationFile}
                        git commit -m "Update manifest for ${BRANC_NAME} to ${IMAGE_TAG} from Jenkins CI" || echo "Nothing to commit"
                        git push origin main
                        """
                    }
                }
            }
        }

        stage('Clean Workspace') {
            steps {
                cleanWs()  
            }
        }
    }
}

