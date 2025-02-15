# Bot de Mensagens Automáticas

Este bot foi desenvolvido para automatizar o envio de mensagens em uma interface web, utilizando Selenium para interagir com o navegador Chrome.

## Requisitos

- Python 3.6 ou superior
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome

## Dependências

As seguintes bibliotecas Python são necessárias:
```
selenium
keyboard
```

## Configuração Inicial

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Inicie o Chrome com debugging remoto:
```bash
google-chrome --remote-debugging-port=9222
```

3. Prepare os arquivos de configuração:

   - `palavras.txt`: Lista de palavras que serão enviadas (uma por linha)
   - `mensagens_iniciais.txt`: Mensagens iniciais no formato `slug|mensagem`

### Formato do arquivo palavras.txt
```
continue
ok
parar
pular
voltar
reiniciar
```

### Formato do arquivo mensagens_iniciais.txt
```
bem-vindo|Olá! Seja bem-vindo ao nosso grupo.
apresentacao|Oi pessoal! Sou o moderador do grupo.
```

## Como Executar

1. Certifique-se de que o Chrome está aberto com a porta de debugging (9222)
2. Execute o script principal:
```bash
python main.py
```

## Comandos Durante a Execução

- Pressione `*` para trocar a palavra atual
- Pressione `Ctrl+C` para encerrar o script

## Funcionalidades

1. **Mensagem Inicial**
   - Ao iniciar, permite selecionar uma mensagem inicial para enviar
   - As mensagens são identificadas por slugs
   - Pode-se pular a mensagem inicial pressionando Enter

2. **Envio Automático**
   - Envia automaticamente as palavras configuradas
   - Detecta quando é possível enviar (ícone de play)
   - Aguarda quando necessário (ícone de stop)

3. **Troca de Palavras**
   - Permite trocar a palavra atual durante a execução
   - Mostra menu com todas as palavras disponíveis
   - Mantém a palavra atual se pressionar Enter

## Tratamento de Erros

- Máximo de 3 falhas consecutivas antes de encerrar
- Tentativas múltiplas para entradas inválidas
- Recuperação automática de alguns tipos de erro
- Feedback claro sobre erros e estado do script

## Estrutura do Projeto

```
├── main.py                     # Script principal
├── requirements.txt            # Dependências do projeto
├── palavras.txt               # Lista de palavras para envio
├── mensagens_iniciais.txt     # Mensagens iniciais com slugs
└── utils/
    ├── driver_manager.py      # Gerenciamento do Selenium
    ├── start_menu_manager.py  # Gerenciamento do Menu Inicial
    ├── keyboard_handler.py    # Monitoramento do teclado
    ├── palavra_manager.py     # Gerenciamento das palavras
    └── mensagem_inicial_manager.py  # Gerenciamento das mensagens iniciais
```

## Regras e Boas Práticas

1. **Segurança**
   - Não compartilhe credenciais ou informações sensíveis
   - Mantenha o ChromeDriver atualizado
   - Use o bot de forma ética e responsável

2. **Uso**
   - Respeite os limites de tempo entre mensagens
   - Não sobrecarregue o sistema com mensagens excessivas
   - Monitore a execução para garantir funcionamento correto

3. **Manutenção**
   - Mantenha os arquivos de texto organizados
   - Atualize as palavras e mensagens conforme necessário
   - Verifique regularmente por atualizações das dependências

## Solução de Problemas

1. **Chrome não conecta**
   - Verifique se o Chrome está rodando com a porta 9222
   - Certifique-se de que não há outras instâncias do Chrome rodando
   - Verifique se o ChromeDriver é compatível com sua versão do Chrome

2. **Mensagens não são enviadas**
   - Verifique a conexão com a internet
   - Confirme se a interface web está carregada corretamente
   - Verifique se há elementos bloqueando o envio

3. **Erros de teclado**
   - Verifique se o script tem permissões necessárias
   - Tente executar como administrador se necessário
   - Verifique se outras aplicações não estão capturando as teclas