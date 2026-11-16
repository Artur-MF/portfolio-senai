[![CI do portfólio](https://github.com/Artur-MF/portfolio-senai/actions/workflows/ci.yml/badge.svg?event=pull_request)](https://github.com/Artur-MF/portfolio-senai/actions/workflows/ci.yml)
[![Deploy no GitHub Pages](https://github.com/Artur-MF/portfolio-senai/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/Artur-MF/portfolio-senai/actions/workflows/deploy.yml)

# Portfólio profissional de Artur Medeiros

Portfólio estático sobre dados, automação e desenvolvimento. [Abrir site no GitHub Pages](https://artur-mf.github.io/portfolio-senai/).

## Validação e publicação

- `index.html`, `style.css` e `images/` contêm o site.
- O workflow [CI](.github/workflows/ci.yml) roda em PRs para `main`, com jobs paralelos em Node.js 22 e 24. Depois do checkout, a primeira checagem exige o `index.html`. Os jobs validam o HTML com HTMLHint, limitam cada arquivo a 500.000 bytes com `find`, verificam termos proibidos nos arquivos do site e checam URLs externas, caminhos de imagens e âncoras.
- O workflow [Deploy](.github/workflows/deploy.yml) roda em cada push para `main`. O job de publicação recebe `pages: write` e `id-token: write`. O artefato contém apenas HTML, CSS e imagens.
- Na regra de proteção de `main`, exija PR, os checks **Linter (Node 22)** e **Linter (Node 24)** e a branch atualizada. Marque também a opção que aplica as restrições a administradores. Em **Settings → Pages → Build and deployment**, selecione **GitHub Actions**.
- Para receber alertas por e-mail, acompanhe o repositório e configure **System → Actions → Email → Only notify for failed workflows** nas [preferências pessoais](https://github.com/settings/notifications). O mesmo menu permite receber também as notificações de sucesso. Cada destinatário pode ativar a opção na própria conta. [Documentação do GitHub](https://docs.github.com/en/subscriptions-and-notifications/how-tos/managing-github-actions-notifications).

## Teste local

Execute `python3 -m http.server 8080` na raiz e acesse `http://localhost:8080`. Para conferir os links, rode `python3 scripts/check_links.py` com os arquivos do site incluídos no Git.
