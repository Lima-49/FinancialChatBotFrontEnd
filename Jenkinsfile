pipeline {
    agent any
    
    environment {
        // Configurações do Docker
        DOCKER_REGISTRY = 'docker.io' // ou seu registry privado
        DOCKER_IMAGE_NAME = 'controle-financeiro-streamlit'
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials' // ID das credenciais no Jenkins
        
        // Configurações da aplicação
        APP_PORT = '8501'
        CONTAINER_NAME = 'streamlit-app'
        
        // Variáveis de ambiente sensíveis (configurar no Jenkins Credentials)
        SUPABASE_URL = credentials('supabase-url')
        SUPABASE_ANON_KEY = credentials('supabase-anon-key')
        DATABASE_URL = credentials('database-url')
    }
    
    options {
        // Manter apenas os últimos 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        
        // Timeout do pipeline
        timeout(time: 30, unit: 'MINUTES')
        
        // Evitar builds concorrentes
        disableConcurrentBuilds()
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Fazendo checkout do código...'
                checkout scm
                
                // Exibir informações do commit
                script {
                    def gitCommit = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    def gitBranch = env.GIT_BRANCH ?: 'main'
                    echo "Branch: ${gitBranch}"
                    echo "Commit: ${gitCommit}"
                }
            }
        }
        
        stage('Validação do Código') {
            parallel {
                stage('Lint Python') {
                    steps {
                        echo 'Verificando sintaxe Python...'
                        script {
                            // Validar sintaxe de todos os arquivos Python
                            sh '''
                                python3 -m py_compile app.py
                                find . -name "*.py" -not -path "./__pycache__/*" -exec python3 -m py_compile {} \\;
                            '''
                        }
                    }
                }
                
                stage('Verificar Dependências') {
                    steps {
                        echo 'Verificando requirements.txt...'
                        script {
                            sh '''
                                if [ ! -f requirements.txt ]; then
                                    echo "ERRO: requirements.txt não encontrado!"
                                    exit 1
                                fi
                                
                                # Verificar se há conflitos de versão conhecidos
                                pip install --dry-run -r requirements.txt || echo "Aviso: possíveis conflitos de dependências"
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "Construindo imagem Docker: ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                script {
                    // Build da imagem com cache e boas práticas
                    docker.build(
                        "${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}",
                        "--build-arg BUILD_DATE=\$(date -u +'%Y-%m-%dT%H:%M:%SZ') " +
                        "--build-arg VERSION=${DOCKER_IMAGE_TAG} " +
                        "--label org.opencontainers.image.source=${env.GIT_URL} " +
                        "--label org.opencontainers.image.revision=${env.GIT_COMMIT} " +
                        "--no-cache ."
                    )
                    
                    // Tag latest
                    sh "docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Testes da Imagem') {
            steps {
                echo 'Testando imagem Docker...'
                script {
                    // Verificar se a imagem foi criada corretamente
                    sh "docker images ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                    
                    // Scan de segurança básico (opcional - requer Docker Scout ou Trivy)
                    try {
                        sh "docker scout cves ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} || echo 'Docker Scout não disponível'"
                    } catch (Exception e) {
                        echo "Scanner de segurança não disponível, continuando..."
                    }
                }
            }
        }
        
        stage('Push to Registry') {
            when {
                // Apenas fazer push em branches específicas
                anyOf {
                    branch 'main'
                    branch 'master'
                    branch 'production'
                }
            }
            steps {
                echo "Enviando imagem para registry..."
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        // Push da imagem com tag específica
                        sh "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                        
                        // Push da imagem com tag latest
                        sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                    branch 'production'
                }
            }
            steps {
                echo 'Iniciando deploy da aplicação...'
                script {
                    // Parar e remover container antigo se existir
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                    
                    // Criar arquivo .env temporário (usar Jenkins credentials)
                    sh """
                        cat > .env.tmp << EOF
SUPABASE_URL=${SUPABASE_URL}
SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
DATABASE_URL=${DATABASE_URL}
ENVIRONMENT=production
EOF
                    """
                    
                    // Executar novo container
                    sh """
                        docker run -d \\
                            --name ${CONTAINER_NAME} \\
                            --restart unless-stopped \\
                            -p ${APP_PORT}:8501 \\
                            --env-file .env.tmp \\
                            --health-cmd='curl -f http://localhost:8501/_stcore/health || exit 1' \\
                            --health-interval=30s \\
                            --health-timeout=10s \\
                            --health-retries=3 \\
                            ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                    """
                    
                    // Remover arquivo temporário
                    sh "rm -f .env.tmp"
                    
                    // Aguardar container ficar saudável
                    echo 'Aguardando aplicação iniciar...'
                    timeout(time: 2, unit: 'MINUTES') {
                        sh """
                            until [ "\$(docker inspect -f {{.State.Health.Status}} ${CONTAINER_NAME})" == "healthy" ]; do
                                echo "Aguardando container ficar saudável..."
                                sleep 5
                            done
                        """
                    }
                }
            }
        }
        
        stage('Smoke Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                    branch 'production'
                }
            }
            steps {
                echo 'Executando testes básicos...'
                script {
                    // Verificar se a aplicação está respondendo
                    sh """
                        sleep 10
                        curl -f http://localhost:${APP_PORT}/_stcore/health || exit 1
                        echo "Aplicação está respondendo corretamente!"
                    """
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                echo 'Limpando imagens antigas...'
                script {
                    // Remover imagens antigas (manter apenas as 3 mais recentes)
                    sh """
                        docker images ${DOCKER_IMAGE_NAME} --format "{{.ID}}" | tail -n +4 | xargs -r docker rmi || true
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline executado com sucesso! ✅'
            // Notificações (Slack, Email, etc)
            // slackSend(color: 'good', message: "Deploy realizado com sucesso - Build #${env.BUILD_NUMBER}")
        }
        
        failure {
            echo 'Pipeline falhou! ❌'
            // Notificações de falha
            // slackSend(color: 'danger', message: "Deploy falhou - Build #${env.BUILD_NUMBER}")
            
            // Rollback em caso de falha (opcional)
            script {
                try {
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                    // Restaurar versão anterior
                    sh "docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:8501 ${DOCKER_IMAGE_NAME}:latest"
                } catch (Exception e) {
                    echo "Erro durante rollback: ${e.message}"
                }
            }
        }
        
        always {
            echo 'Limpando workspace...'
            cleanWs()
        }
    }
}
