BRANCH_NAME = env.BRANCH_NAME.replaceAll('/', '-').stripIndent()
RELEASE_BRANCH = "master"
TAG_NAME = ""
PROJECT = "button3d"




node('docker'){
try {
    stage('Setup'){
        // set & clean up git local version of git repo
        checkout scm
        helpers.ECRLogin()
    }

    stage('Build'){
        sh "make artifact/docker"
    }
    stage('TagAndPublish'){
        helpers.retagAndPushImage("vaultify", BRANCH_NAME, TAG_NAME)
    }
    stage('Deploy'){
        println "not implemented yet"
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