BRANCH_NAME = env.BRANCH_NAME.replaceAll('/', '-').stripIndent()
RELEASE_BRANCH = "master"
TAG_NAME = "0.1.1"
PROJECT = "vaultify"
BASE_IMAGE = 3.7-alpine3.9

node('docker'){
    try {
        stage('Setup'){
            // set & clean up git local version of git repo
            checkout scm
            helpers.ECRLogin()
        }

        stage('Build'){
            sh "docker build --build-arg BASE_IMAGE=${BASE_IMAGE} -t vaultify:${TAG_NAME} --target prod ."
        }
        stage('TagAndPublish'){
            helpers.retagAndPushImage("vaultify", TAG_NAME, TAG_NAME)
        }
    } catch (e) {
        println "error occured: ${e}"
        throw(e)
    } finally {
        stage('Parse Tests'){
            junit "**/test-reports/*.xml"
        }
    }
}