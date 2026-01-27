# 🚀 Guia de Deploy - Controle Financeiro

Este guia detalha como fazer o deploy da aplicação Streamlit usando Jenkins e Docker.

## 📋 Pré-requisitos

### 1. Jenkins
- Jenkins instalado e configurado
- Plugins necessários:
  - Docker Pipeline
  - Git Plugin
  - Credentials Plugin
  - Pipeline Plugin

### 2. Docker
- Docker instalado no servidor Jenkins
- Docker Compose (opcional)
- Acesso ao Docker Registry (Docker Hub ou privado)

### 3. Credenciais no Jenkins
Configure as seguintes credenciais no Jenkins (Manage Jenkins > Credentials):

| ID da Credencial | Tipo | Descrição |
|-----------------|------|-----------|
| `docker-hub-credentials` | Username/Password | Credenciais do Docker Hub |
| `supabase-url` | Secret Text | URL do Supabase |
| `supabase-anon-key` | Secret Text | Chave anônima do Supabase |
| `database-url` | Secret Text | String de conexão do PostgreSQL |

## 🏗️ Arquitetura do Pipeline

```
Checkout → Validação → Build Docker → Testes → Push Registry → Deploy → Smoke Tests → Cleanup
```

### Etapas do Pipeline:

1. **Checkout**: Clone do repositório
2. **Validação**: Lint Python e verificação de dependências
3. **Build Docker**: Criação da imagem Docker otimizada
4. **Testes da Imagem**: Verificações de segurança
5. **Push to Registry**: Envio para Docker Registry (apenas branches específicas)
6. **Deploy**: Deploy do container
7. **Smoke Tests**: Testes básicos de saúde
8. **Cleanup**: Limpeza de imagens antigas

## 🐳 Docker

### Build Manual

```bash
# Build da imagem
docker build -t controle-financeiro-streamlit:latest .

# Executar localmente
docker run -d \
  --name streamlit-app \
  -p 8501:8501 \
  --env-file .env \
  controle-financeiro-streamlit:latest
```

### Docker Compose

```bash
# Subir aplicação
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar aplicação
docker-compose down
```

## ⚙️ Configuração do Jenkins

### 1. Criar Job no Jenkins

1. Acesse Jenkins → New Item
2. Digite o nome do projeto
3. Selecione "Pipeline"
4. Clique em OK

### 2. Configurar Pipeline

Na seção Pipeline:
- **Definition**: Pipeline script from SCM
- **SCM**: Git
- **Repository URL**: URL do seu repositório
- **Branch**: `*/main` (ou sua branch principal)
- **Script Path**: `Jenkinsfile`

### 3. Configurar Webhooks (Opcional)

Para builds automáticos:
1. No Jenkins: Configure → Build Triggers → GitHub hook trigger
2. No GitHub: Settings → Webhooks → Add webhook
3. URL: `http://seu-jenkins:8080/github-webhook/`

## 🔧 Variáveis de Ambiente

### Produção (.env)
```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua-chave-anonima
DATABASE_URL=postgresql://usuario:senha@host:5432/database
ENVIRONMENT=production
```

### Desenvolvimento
```env
ENVIRONMENT=development
```

## 📊 Monitoramento

### Health Check
```bash
# Verificar saúde da aplicação
curl http://localhost:8501/_stcore/health

# Verificar status do container
docker inspect --format='{{.State.Health.Status}}' streamlit-app
```

### Logs
```bash
# Logs do container
docker logs -f streamlit-app

# Logs do Docker Compose
docker-compose logs -f streamlit-app
```

## 🔐 Boas Práticas de Segurança

1. **Não commitar .env**: Sempre use Jenkins Credentials
2. **Usuário não-root**: Container roda com usuário `streamlit`
3. **Multi-stage build**: Imagem otimizada e menor
4. **Health checks**: Monitoramento automático
5. **Scan de segurança**: Verificação de vulnerabilidades
6. **HTTPS**: Use reverse proxy (Nginx/Traefik) com SSL

## 🚨 Troubleshooting

### Container não inicia
```bash
# Verificar logs
docker logs streamlit-app

# Verificar variáveis de ambiente
docker exec streamlit-app env | grep SUPABASE
```

### Erro de conexão com banco
```bash
# Testar conexão do container
docker exec -it streamlit-app psql $DATABASE_URL -c "SELECT 1"
```

### Build falha no Jenkins
1. Verificar logs do Jenkins
2. Verificar se Docker daemon está rodando
3. Verificar credenciais configuradas
4. Verificar se usuário Jenkins tem permissões Docker

### Porta já em uso
```bash
# Encontrar processo usando a porta
netstat -tlnp | grep 8501

# Parar container antigo
docker stop streamlit-app
docker rm streamlit-app
```

## 🔄 Rollback

### Automático
O pipeline realiza rollback automático em caso de falha no deploy.

### Manual
```bash
# Listar versões disponíveis
docker images controle-financeiro-streamlit

# Executar versão anterior
docker run -d \
  --name streamlit-app \
  -p 8501:8501 \
  --env-file .env \
  controle-financeiro-streamlit:VERSAO_ANTERIOR
```

## 📈 Otimizações

### Build mais rápido
- Use cache de layers Docker
- `.dockerignore` configurado corretamente
- Multi-stage build implementado

### Performance
- Limite de recursos configurado no docker-compose
- Health checks otimizados
- FileWatcher desabilitado em produção

## 🌐 Acesso à Aplicação

Após o deploy bem-sucedido:
- **Local**: http://localhost:8501
- **Produção**: Configure um reverse proxy (Nginx) com domínio e SSL

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs do Jenkins
2. Verifique os logs do container
3. Revise as configurações de credenciais
4. Consulte a documentação do Streamlit

## 🎯 Checklist de Deploy

- [ ] Jenkins configurado com plugins necessários
- [ ] Credenciais configuradas no Jenkins
- [ ] Docker instalado e funcionando
- [ ] Jenkinsfile no repositório
- [ ] Dockerfile testado localmente
- [ ] .dockerignore configurado
- [ ] Variáveis de ambiente configuradas
- [ ] Health checks funcionando
- [ ] Testes básicos passando
- [ ] Monitoramento configurado
- [ ] Backup configurado (banco de dados)
- [ ] SSL/HTTPS configurado (produção)

## 📚 Recursos Adicionais

- [Documentação Streamlit](https://docs.streamlit.io/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Supabase Documentation](https://supabase.com/docs)
