# Roteiro para Inicializar o Docker

## Necessário:
- Docker instalado
- Docker Compose instalado

---

## 1️ Criar as Chaves Necessárias
Antes de iniciar os containers, é preciso criar as secrets que serão usadas na aplicação.

### **Linux**
```bash
echo "minha_suap_key" | docker secret create suap_key -
echo "minha_suap_secret" | docker secret create suap_secret -
```

### **Windows (PowerShell)**
```powershell
echo "minha_suap_key" | docker secret create suap_key -
echo "minha_suap_secret" | docker secret create suap_secret -
```

Verifique se foram criadas corretamente:
```bash
docker secret ls
```

Se precisar remover um secret:
```bash
docker secret rm suap_key

docker secret rm suap_secret
```

---

## 2️ Iniciar o Docker Swarm
O Docker Swarm precisa estar ativo para que os secrets sejam utilizados corretamente.

### **Linux & Windows (PowerShell)**
Inicialize o Swarm:
```bash
docker swarm init
```

Verifique se o Swarm está rodando:
```bash
docker info | grep Swarm
```

Se precisar resetar o Swarm:
```bash
docker swarm leave --force
```
E depois inicialize novamente.

---

## 3️ Criar as Imagens Docker

### Criar a imagem do backend (`web`)
Certifique-se de que seu `Dockerfile` está configurado corretamente e, na raiz do projeto, execute:
```bash
docker build -t labstock_web:latest .
```

Verifique se as imagens foram criadas:
```bash
docker images
```

---

## 4️ Subir os Containers
Com as secrets criadas e as imagens prontas, podemos rodar o `docker-compose`:
```bash
docker-compose up -d
```
Isso iniciará os containers em modo "detached" (em segundo plano).

Verifique se os containers estão rodando:
```bash
docker ps
```

Se precisar visualizar os logs:
```bash
docker-compose logs -f
```

---

## Parar e Remover Containers
Se precisar parar e remover os containers:
```bash
docker-compose down
```
Para remover também os volumes:
```bash
docker-compose down -v
```

---


