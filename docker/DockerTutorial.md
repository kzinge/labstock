# Roteiro para Inicializar o Docker
 Para o projeto Labstock

## Necessário:
- Docker instalado
- Docker Compose instalado

---

## 1. Iniciar o Docker Swarm
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

## 2. Criar as Chaves Necessárias
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

## 3. Criar as Imagens Docker

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

## 4. Rodar os Containers com Docker Stack
Com as secrets criadas e as imagens prontas, podemos rodar o `docker stack` para iniciar os containers no Swarm:

```bash
docker stack deploy -c docker-compose.yml labstock
```

Verifique se os services estão rodando:
```bash
docker stack services labstock
```

Para visualizar os logs:
```bash
docker service logs -f labstock_web
```

---

## EXTRAS

## Parar e Remover Containers
Se precisar remover o stack:
```bash
docker stack rm labstock
```

Para remover os secrets criados:
```bash
docker secret rm suap_key suap_secret
```

Se precisar resetar o Swarm:
```bash
docker swarm leave --force
```

