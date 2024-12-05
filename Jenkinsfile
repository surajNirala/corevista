pipeline {
    agent any 

    environment {
        DOCKER_HUB_REPO = 'snirala1995/corevista'
        DOCKER_IMAGE_TAG = "${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"
        CONTAINER_NAME = 'corevista' // Name for your Docker container
        CONTAINER_PORT = '8000' // Port inside the Docker container
        CREDENTIAL_SNIRALA_DOCKERHUB = 'credentials-snirala-dockerhub'
        CREDENTIALS_GOLANG_SERVER = 'credentials-golang-server'
        JENKINS_SERVER = '35.200.176.111'
        GOLANG_SERVER = '34.131.166.50'
        DATABASE_VOLUME = '/home/srj/db/:/app/db' 
    }

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['Dev', 'Live'], description: 'Select The Environment')
    }

    stages {
        stage('Set Ports') {
            steps {
                script {
                    // Set ports based on the selected environment
                    if (params.ENVIRONMENT == 'Dev') {
                        env.HOST_PORT = '8006'
                        env.SERVER_IP = "http://${GOLANG_SERVER}:${env.HOST_PORT}"
                    } else if (params.ENVIRONMENT == 'Live') {
                        env.HOST_PORT = '8007'
                        env.SERVER_IP = "http://${GOLANG_SERVER}:${env.HOST_PORT}"
                    }
                }
            }
        }
        /*  stage('Code Analysis') {
                environment {
                    scannerHome = tool 'Sonar-Scanner'
                }
                steps {
                    script {
                        withSonarQubeEnv('Sonar-Scanner') {
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=workwebui \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=https://sonarqube.dhimalu.xyz \
                                -Dsonar.login=sqp_c6b396ecc795e7b4e16eb2a48b015d326baf1477
                            """
                        }
                    }
                }
            } 
        */
        /* stage('Check Existing Container') {
            steps {
                script {
                    echo "Checking if the container already exists"
                    def existingContainer = sh(script: "docker ps -aqf name=${CONTAINER_NAME}-${env.HOST_PORT}", returnStdout: true).trim()
                    if (existingContainer) {
                        echo "Stopping and removing the existing container: ${CONTAINER_NAME}-${env.HOST_PORT}"
                        sh "docker rm -f ${CONTAINER_NAME}-${env.HOST_PORT}"
                    }
                }
            }
        } */

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building the Docker image"
                    docker.build(DOCKER_IMAGE_TAG)
                    echo "Docker image built successfully."
                }
            }
        }

        stage('Push Docker Image To Docker Hub') {
            steps {
                script {
                    try {
                        echo "Pushing Docker image to DockerHub."
                        docker.withRegistry('https://registry.hub.docker.com', CREDENTIAL_SNIRALA_DOCKERHUB) {
                            docker.image(DOCKER_IMAGE_TAG).push()
                        }
                        echo "Docker image pushed to DockerHub successfully."
                    } catch (Exception e) {
                        echo "Failed to push Docker image: ${e.message}"
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    if (params.ENVIRONMENT == 'Dev' || params.ENVIRONMENT == 'Live') {
                        echo "Deploying to ================= SRJ-SERVER ============== (${GOLANG_SERVER})"
                        sshagent([CREDENTIALS_GOLANG_SERVER]) {
                            echo "Deploying to ${GOLANG_SERVER} on port ${HOST_PORT} with image ${DOCKER_IMAGE_TAG}"
                            withCredentials([usernamePassword(credentialsId: CREDENTIAL_SNIRALA_DOCKERHUB, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]){
                            sh """
                                echo "Connecting to ${GOLANG_SERVER}..."
                                ssh -o StrictHostKeyChecking=no srj@${GOLANG_SERVER} <<EOF
                                echo "Remote server connected successfully!"

                                # Docker login
                                echo "Logging into DockerHub"
                                echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin || { echo "Docker login failed"; exit 1; }

                                # Pull the latest image if not available locally
                                echo "Pulling Docker image from DockerHub: ${DOCKER_IMAGE_TAG}"
                                docker pull ${DOCKER_IMAGE_TAG}

                                # Check and stop/remove the existing container
                                existing_container=$(docker ps -a --filter "name=${CONTAINER_NAME}-${HOST_PORT}" -q)
                                if [ -n "$existing_container" ]; then
                                    echo "Stopping and removing the existing container: ${CONTAINER_NAME}-${HOST_PORT}"
                                    docker rm -f ${CONTAINER_NAME}-${HOST_PORT} || { echo "Failed to remove container"; exit 1; }
                                else
                                    echo "No existing container found."
                                fi

                                # Run the new Docker container on the same port
                                echo "Running the Docker container"
                                docker run -d --init -p ${HOST_PORT}:${CONTAINER_PORT} -v ${DATABASE_VOLUME} --name ${CONTAINER_NAME}-${HOST_PORT} ${DOCKER_IMAGE_TAG} || { echo "Failed to run the container"; exit 1; }

                                echo "Docker image ${DOCKER_IMAGE_TAG} run successfully."
                                exit
                            """
                            // docker run --env-file ${ENV_FINAL_LIVE} -d --init -p ${HOST_PORT}:${CONTAINER_PORT} --name ${CONTAINER_NAME}-${HOST_PORT} ${DOCKER_IMAGE_TAG}
                            }
                        }
                    } else {
                        echo "Deploying image in non-Dev environment"
                        sh "docker run -d --init -p ${HOST_PORT}:${CONTAINER_PORT} --name ${CONTAINER_NAME}-${HOST_PORT} ${DOCKER_IMAGE_TAG}"
                        echo "Docker image ${DOCKER_IMAGE_TAG} run successfully."
                    }   
                }
            }
        }
    }

    post {
        success {
            script {
                echo "Docker image ${DOCKER_IMAGE_TAG} successfully pushed to Docker Hub."
                echo "Container running on port: ${HOST_PORT}"
                echo "Pipeline completed successfully."
                echo "Click the following link to check the website live: ${env.SERVER_IP}"
            }
        }
        failure {
            script {
                echo "Pipeline failed. Check logs for details."
            }
        }
    }
}
