pipeline {
    agent any

    environment {
        REGISTRY = "harbor-uqi.boer.id/ci-cd"
        IMAGE_NAME = "flask-crud"
        IMAGE_TAG = "${BUILD_NUMBER}"
        MANIFEST_REPO = "https://github.com/luqinthar/todo-manifest.git"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm // Automatically checks out the branch being built
            }
        }
        stage('Build and Push Docker Image') {
            steps {
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
                    git branch: "${BRANCH_NAME}", url: "${MANIFEST_REPO}", credentialsId: 'github'

                    script {
                        def kustomizationFile = "overlays/${BRANCH_NAME}/kustomization.yaml"
                        sh """
                        echo "Updating image in ${kustomizationFile}"
                        sed -i "s|newName:.*|newName: ${REGISTRY}/${IMAGE_NAME}|" ${kustomizationFile}
                        sed -i "s|newTag:.*|newTag: ${IMAGE_TAG}-${BRANCH_NAME}|" ${kustomizationFile}

                        git config user.email "jenkins-uqi@keyz.my.id"
                        git config user.name "Jenkins CI"

                        git add ${kustomizationFile}
                        git commit -m "Update manifest for ${BRANCH_NAME} to ${IMAGE_TAG} from Jenkins CI" || echo "Nothing to commit"
                        git pull --rebase origin ${BRANCH_NAME} || echo "No changes to pull"
                        git push origin ${BRANCH_NAME}
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
