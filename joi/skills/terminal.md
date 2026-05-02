skill name: terminal
gatilhos: terminal, shell, bash, comando, executar, rodar, rodar comando, executar comando, instalar, instalação, pacote, apt, apt-get, pip, npm, brew, yum, dnf, snap, pacman, sistema, processo, processo, matar processo, kill, ps, top, htop, cpu, memória, ram, disco, espaço, df, du, free, rede, ping, dns, ip, ifconfig, curl, wget, download, git, clone, commit, push, pull, branch, docker, container, serviço, service, systemctl, daemon, reiniciar, restart, parar, stop, iniciar, start, sudo, root, permisso, permissão, chmod, chown, link simbólico, symlink, ln, copiar, cp, mover, mv, remover, rm, deletar, excluir, criar diretório, mkdir, zip, tar, compactar, extrair, descompactar, script, bash script, cron, agendar, update, upgrade, atualizar, atualização, sistema operacional, distro, kernel, driver, dependência, lib, biblioteca, compilar, make, gcc, build, configurar, config, ambiente, variável de ambiente, export, fonte, source, alias, path, ssh, remoto, servidor, localhost, porta, firewall, iptables, ufw, logs, journalctl, dmesg, histórico, history, which, whereis, locate, find, grep, sed, awk, cat, head, tail, less, more, echo, printf, env, printenv
prioridade: alta

# Terminal

## REGRA PRINCIPAL
Se não houver uma tool ESPECÍFICA para a tarefa, use SEMPRE o terminal.
Ele é a ferramenta mais versátil e resolve qualquer coisa que as outras não cobrem.

## O que o terminal pode fazer
- Instalar pacotes e aplicativos (apt, pip, npm, snap, etc.)
- Gerenciar arquivos e diretórios (criar, copiar, mover, deletar)
- Executar scripts e programas
- Monitorar sistema (processos, memória, disco, rede)
- Configurar ambiente (variáveis, aliases, paths)
- Operações git (clone, push, pull, commit)
- Qualquer comando Linux que exista

## Regras
1. PREFIRA o terminal a qualquer tool menos específica
2. Use sudo quando necessário — a senha é automática
3. Se o comando falhar, tente entender o erro e corrija
4. Comandos destrutivos (rm -rf) peça confirmação
5. Explique BREVEMENTE o que fez após executar
