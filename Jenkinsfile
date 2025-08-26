pipeline {
  agent any
  environment {
    // Jenkins 서비스 계정(jenkins)의 pipx 경로 포함
    PATH = "/usr/local/bin:/usr/bin:/bin:/var/lib/jenkins/.local/bin:${PATH}"
  }
  options { timestamps(); ansiColor('xterm') }
  // NAT 환경: 웹훅 대신 2분마다 Git 변경 체크
  triggers { pollSCM('H/2 * * * *') }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Bandit (SAST)') {
      steps {
        sh 'bandit -r . -f json -o bandit.json || true'
      }
      post { always { archiveArtifacts "bandit.json" } }
    }

    stage('pip-audit (Dependencies)') {
      steps {
        sh 'pip-audit -r requirements.txt -f json -o pip-audit.json || true'
      }
      post { always { archiveArtifacts "pip-audit.json" } }
    }

    stage('Gate (간단 실패 기준)') {
      steps {
        sh '''
          # Bandit 결과에서 HIGH 심각도 있으면 실패
          if jq -e '.results[]?|select(.issue_severity=="HIGH")' bandit.json >/dev/null 2>&1; then
            echo "Bandit HIGH severity found"; exit 1; fi
          # 의존성 취약점 1개라도 있으면 실패
          if [ "$(jq '.vulnerabilities|length' pip-audit.json 2>/dev/null || echo 0)" -gt 0 ]; then
            echo "Dependency vulnerabilities found"; exit 1; fi
        '''
      }
    }
  }

  post {
    success { echo '✅ No blocking issues.' }
    failure { echo '❌ Blocking issues detected.' }
    always  { echo 'Reports archived: bandit.json, pip-audit.json' }
  }
}
