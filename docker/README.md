# Diretório `docker`

Este diretório é responsável por armazenar todos os arquivos relacionados à **containerização** e **orquestração** do projeto. Abaixo você encontra a descrição de cada arquivo e subpasta.

---

## Estrutura

docker
├── docker-compose.yml
├── dockerfile
├── DockerTutorial.md
├── nginx
│   └── default.conf
└── README.md

## Descrição dos Arquivos

- **docker-compose.yml**  
  Arquivo de orquestração de containers. Ele define e gerencia múltiplos serviços como aplicação, banco de dados, servidor web, entre outros, facilitando o deploy com apenas um comando (`docker-compose up`).

- **dockerfile**  
  Arquivo de instruções para criação da imagem Docker personalizada da aplicação.  
  Ele define o ambiente que a aplicação precisa para rodar, como o sistema base, bibliotecas e dependências.

- **DockerTutorial.md**  
  Documento com explicações, comandos úteis e boas práticas sobre o uso do Docker no contexto deste projeto. Ideal para consulta rápida ou para quem está começando com Docker.

---

## Subdiretório `nginx`

- **nginx/default.conf**  
  Arquivo de configuração padrão do Nginx utilizado como proxy reverso.  
  Esse arquivo define como o Nginx irá redirecionar as requisições HTTP para os containers da aplicação, além de configurações de segurança e otimização.

---