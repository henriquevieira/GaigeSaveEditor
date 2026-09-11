# GaigeSaveEditor

🇺🇸 [English](#english) | 🇧🇷 [Português](#português)

A modern, open-source Borderlands 2 save editor written in Python, with a focus on Linux, Steam and Proton.

> **Project status:** Early development.
> GaigeSaveEditor is being built incrementally, starting with save detection, parsing, backup and basic character editing.

---

# English

## About

**GaigeSaveEditor** is an open-source save editor for **Borderlands 2**, written in Python.

The project aims to provide a modern and Linux-friendly alternative for inspecting and modifying Borderlands 2 character save files, with particular attention to players running the Windows version of the game through **Steam Proton**.

The initial goal is to provide a reliable command-line tool capable of locating save files, creating backups, reading character information and safely modifying basic properties such as character level and experience.

A graphical interface may be added in the future.

## Why GaigeSaveEditor?

Existing Borderlands 2 save editors have been extremely useful to the community, but many were originally developed years ago using technologies and workflows primarily targeting Windows.

GaigeSaveEditor aims to explore a different approach:

* Python 3
* Linux-friendly development
* Steam Proton support
* Simple command-line interface
* Automatic backups
* Modular architecture
* Automated tests
* Cross-platform potential
* Open-source development

The project is also intended as an exploration and documentation of the Borderlands 2 save format.

## Planned features

### Initial version

* Automatically locate Borderlands 2 saves from Steam/Proton
* Discover available characters
* Read basic character information
* Display character name
* Display character class
* Display current level and experience
* Create automatic backups before modifications
* Change character level
* Adjust experience consistently with the selected level
* Validate the save after modification

### Future versions

Possible future features include:

* Money editing
* Eridium editing
* Seraph Crystal editing
* Torgue Token editing
* Skill point editing
* Inventory inspection
* Weapon and item editing
* Item level adjustment
* Mission inspection
* Fast Travel inspection
* Raw save information
* Graphical interface
* Windows support improvements
* Steam Deck support

The roadmap may change as the save format and existing implementations are studied.

## Planned CLI

The command-line interface is expected to follow a simple structure.

### Find characters

```bash
gaige list
```

Example:

```text
ID   Save           Character    Class        Level
1    Save0001.sav   Gaige        Mechromancer 23
2    Save0002.sav   Maya         Siren        17
```

### Character information

```bash
gaige info Save0001.sav
```

Expected output:

```text
Save:       Save0001.sav
Character:  Gaige
Class:      Mechromancer
Level:      23
Experience: 123456
```

### Change level

```bash
gaige level Save0001.sav 50
```

Expected behavior:

```text
Save: Save0001.sav

Level:
23 -> 50

Backup created.
Experience updated.
Save rebuilt.
Save validation successful.
```

## Save location

When Borderlands 2 is running through Steam Proton, save files are normally available somewhere inside the Proton prefix associated with Steam App ID `49520`.

A common location is:

```text
~/.local/share/Steam/steamapps/compatdata/49520/pfx/
```

GaigeSaveEditor aims to detect common Steam installations automatically instead of requiring the user to locate the save directory manually.

Support for installations such as Flatpak may also be added.

## Safety

Editing save files always carries some risk.

GaigeSaveEditor should therefore:

1. Never modify a save without creating a backup.
2. Preserve the original save whenever possible.
3. Validate reconstructed save data before replacing the active file.
4. Allow users to specify save files manually.
5. Clearly report errors instead of writing partially generated data.

Even with these precautions, users should keep their own backups of important characters.

## Technical goals

The project will initially target:

```text
Python 3.11+
```

Possible dependencies include:

* Protocol Buffers
* Typer or Click
* Rich
* pytest

The exact dependency set will be decided as the implementation evolves.

## Proposed architecture

```text
GaigeSaveEditor/
├── README.md
├── LICENSE
├── pyproject.toml
├── src/
│   └── gaige/
│       ├── __init__.py
│       ├── cli.py
│       ├── proton.py
│       ├── save.py
│       ├── backup.py
│       ├── compression.py
│       ├── checksum.py
│       └── protobuf/
└── tests/
```

The save-handling code should remain independent from the CLI so that other interfaces can be added later.

For example:

```text
                 ┌───────────────┐
                 │      CLI      │
                 └───────┬───────┘
                         │
                  ┌──────▼──────┐
                  │ Gaige Core  │
                  └──────┬──────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   Save Parser      Save Writer     Proton Finder
        │                │                │
   Protobuf /        Validation       Steam saves
   compression       and backup
```

This separation should make it possible to eventually provide interfaces such as:

```text
CLI
 │
 ├── Terminal
 │
 ├── Desktop GUI
 │
 └── other integrations
 │
 ▼
GaigeSaveEditor Core
```

## Development roadmap

The first milestone is intentionally small.

**v0.1 — Read saves**

Locate Borderlands 2 saves and extract basic character information.

**v0.2 — Safe editing**

Automatic backups and character level/experience modification.

**v0.3 — Resources**

Money, Eridium and other character resources.

**v0.4 — Inventory**

Read and modify weapons and items.

**v0.5 — GUI prototype**

Optional graphical interface built on top of the same Python core.

## Inspiration and prior work

GaigeSaveEditor does not attempt to ignore the work already done by the Borderlands community.

Existing open-source projects provide valuable information about the Borderlands 2 save format and can serve as references while developing and validating this implementation.

In particular:

* Gibbed's Borderlands 2 Save Editor
* Existing community research into the Borderlands save format
* Previous Python implementations and experiments

Where code is reused or adapted, the corresponding licenses and attribution requirements must be respected.

The goal is to create a modern implementation while properly crediting prior work.

## Contributing

The project is currently in an experimental stage.

Contributions, testing, documentation improvements and research into the Borderlands 2 save format will be welcome once the basic architecture is established.

## Disclaimer

GaigeSaveEditor is an unofficial community project.

It is not affiliated with, endorsed by, or sponsored by Gearbox Software, 2K Games, Take-Two Interactive or Valve.

Borderlands, Borderlands 2 and related names and trademarks belong to their respective owners.

Use this software at your own risk and always keep backups of your save files.

## Installing and developing with `pyproject.toml`

GaigeSaveEditor uses `pyproject.toml` as the main Python project configuration file.

It defines project metadata, supported Python versions, runtime dependencies, development dependencies, CLI entry points and tool configuration.

This means that, for normal development, a separate `requirements.txt` file is not required.

### Create a virtual environment

From the project root:

```bash
python -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### Upgrade pip

Before installing the project, it is recommended to update `pip`:

```bash
python -m pip install --upgrade pip
```

### Install GaigeSaveEditor

To install the project and its runtime dependencies:

```bash
pip install .
```

This reads the dependencies declared in:

```toml
[project]
dependencies = [
    ...
]
```

inside `pyproject.toml`.

### Install in editable mode

During development, the recommended installation mode is:

```bash
pip install -e .
```

The `-e` option means **editable installation**.

With an editable installation, changes made to the source code are immediately available without reinstalling the package after every modification.

For example, after editing:

```text
src/gaige/cli.py
```

the updated code will already be used by:

```bash
gaige
```

### Install development dependencies

GaigeSaveEditor defines additional development tools under:

```toml
[project.optional-dependencies]
dev = [
    ...
]
```

To install the project together with the development dependencies:

```bash
pip install -e ".[dev]"
```

This is the recommended command for contributors and local development.

It installs:

* GaigeSaveEditor
* Runtime dependencies
* Test dependencies
* Linting and development tools

### Verify the installation

After installation:

```bash
gaige --help
```

should display the available commands.

The installed version can be checked with:

```bash
gaige version
```

### Run tests

The test suite uses `pytest`.

Run all tests with:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_proton.py
```

Run a specific test:

```bash
pytest tests/test_proton.py::test_find_proton_prefix
```

### Test coverage

If `pytest-cov` is installed:

```bash
pytest --cov=gaige
```

A more detailed report can be generated with:

```bash
pytest --cov=gaige --cov-report=term-missing
```

### Code linting

GaigeSaveEditor uses Ruff for code quality checks.

Run:

```bash
ruff check .
```

Ruff can automatically fix some issues:

```bash
ruff check . --fix
```

### Code formatting

If Ruff formatting is enabled in the project:

```bash
ruff format .
```

To only verify formatting without modifying files:

```bash
ruff format --check .
```

### Build the package

GaigeSaveEditor can also be built as a standard Python package.

First install the `build` package if necessary:

```bash
pip install build
```

Then run:

```bash
python -m build
```

The generated packages will be placed in:

```text
dist/
```

Typically:

```text
dist/
├── gaige_save_editor-0.1.0-py3-none-any.whl
└── gaige_save_editor-0.1.0.tar.gz
```

### Install the generated package

The generated wheel can be installed directly:

```bash
pip install dist/gaige_save_editor-0.1.0-py3-none-any.whl
```

This is useful for testing the package in an environment closer to what an end user would receive.

### Uninstall

To remove GaigeSaveEditor from the current Python environment:

```bash
pip uninstall gaige-save-editor
```

### Recommended development workflow

A typical development setup is:

```bash
git clone <repository-url>
cd GaigeSaveEditor

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -e ".[dev]"

gaige --help
pytest
ruff check .
```

After this setup, the project is ready for development.

### Useful `pip` commands

Show information about the installed package:

```bash
pip show gaige-save-editor
```

List installed packages:

```bash
pip list
```

Check for dependency conflicts:

```bash
pip check
```

Reinstall the project if necessary:

```bash
pip install --force-reinstall .
```

For development, however, prefer:

```bash
pip install -e ".[dev]"
```

because editable mode avoids unnecessary reinstalls.

---

# Português

## Sobre

**GaigeSaveEditor** é um editor open-source de arquivos de save do **Borderlands 2**, desenvolvido em Python.

O projeto tem como objetivo fornecer uma alternativa moderna e amigável ao Linux para visualizar e modificar os saves dos personagens de Borderlands 2, com atenção especial aos jogadores que executam a versão Windows do jogo através do **Steam Proton**.

O objetivo inicial é disponibilizar uma ferramenta de linha de comando confiável, capaz de localizar os saves, criar backups, ler informações dos personagens e modificar com segurança propriedades básicas, como nível e experiência.

Uma interface gráfica poderá ser adicionada futuramente.

## Por que GaigeSaveEditor?

Os editores de save existentes para Borderlands 2 foram extremamente importantes para a comunidade, mas muitos deles foram originalmente desenvolvidos há vários anos, utilizando tecnologias e fluxos de trabalho voltados principalmente ao Windows.

O GaigeSaveEditor pretende explorar uma abordagem diferente:

* Python 3
* Desenvolvimento amigável ao Linux
* Suporte ao Steam Proton
* Interface de linha de comando simples
* Backups automáticos
* Arquitetura modular
* Testes automatizados
* Potencial multiplataforma
* Desenvolvimento open-source

O projeto também pretende servir como uma exploração e documentação do formato de save utilizado pelo Borderlands 2.

## Funcionalidades planejadas

### Versão inicial

* Localizar automaticamente os saves do Borderlands 2 no Steam/Proton
* Identificar os personagens disponíveis
* Ler informações básicas do personagem
* Exibir nome do personagem
* Exibir classe
* Exibir nível e experiência atuais
* Criar backups automáticos antes de qualquer modificação
* Alterar o nível do personagem
* Ajustar a experiência de forma consistente com o nível escolhido
* Validar o save depois da modificação

### Versões futuras

Algumas funcionalidades que poderão ser implementadas:

* Alteração de dinheiro
* Alteração de Eridium
* Alteração de Seraph Crystals
* Alteração de Torgue Tokens
* Alteração de pontos de habilidade
* Visualização do inventário
* Edição de armas e itens
* Ajuste do nível dos equipamentos
* Visualização de missões
* Visualização de Fast Travel
* Visualização dos dados brutos do save
* Interface gráfica
* Melhor suporte ao Windows
* Suporte ao Steam Deck

O roadmap poderá ser alterado conforme avançar o estudo do formato dos saves e das implementações existentes.

## CLI planejada

A interface de linha de comando deverá seguir uma estrutura simples.

### Encontrar personagens

```bash
gaige list
```

Exemplo:

```text
ID   Save           Personagem   Classe        Nível
1    Save0001.sav   Gaige        Mechromancer  23
2    Save0002.sav   Maya         Siren         17
```

### Informações do personagem

```bash
gaige info Save0001.sav
```

Saída esperada:

```text
Save:        Save0001.sav
Personagem:  Gaige
Classe:      Mechromancer
Nível:       23
Experiência: 123456
```

### Alterar nível

```bash
gaige level Save0001.sav 50
```

Comportamento esperado:

```text
Save: Save0001.sav

Nível:
23 -> 50

Backup criado.
Experiência atualizada.
Save reconstruído.
Validação concluída com sucesso.
```

## Localização dos saves

Quando Borderlands 2 é executado através do Steam Proton, os arquivos de save normalmente ficam dentro do prefixo Proton correspondente ao Steam App ID `49520`.

Uma localização comum é:

```text
~/.local/share/Steam/steamapps/compatdata/49520/pfx/
```

O objetivo do GaigeSaveEditor é localizar automaticamente as instalações mais comuns do Steam, evitando que o usuário precise encontrar manualmente o diretório dos saves.

Também poderá ser incluído suporte para instalações através de Flatpak.

## Segurança

Modificar arquivos de save sempre apresenta algum risco.

Por esse motivo, o GaigeSaveEditor deverá:

1. Nunca modificar um save sem criar um backup.
2. Preservar o arquivo original sempre que possível.
3. Validar os dados reconstruídos antes de substituir o save ativo.
4. Permitir que o usuário informe manualmente um arquivo.
5. Informar claramente os erros em vez de gravar dados parcialmente gerados.

Mesmo com essas proteções, é recomendado manter backups próprios dos personagens importantes.

## Objetivos técnicos

Inicialmente, o projeto deverá utilizar:

```text
Python 3.11+
```

Possíveis dependências:

* Protocol Buffers
* Typer ou Click
* Rich
* pytest

A lista definitiva de dependências será definida conforme a implementação avançar.

## Arquitetura proposta

```text
GaigeSaveEditor/
├── README.md
├── LICENSE
├── pyproject.toml
├── src/
│   └── gaige/
│       ├── __init__.py
│       ├── cli.py
│       ├── proton.py
│       ├── save.py
│       ├── backup.py
│       ├── compression.py
│       ├── checksum.py
│       └── protobuf/
└── tests/
```

A lógica responsável pelos saves deverá permanecer independente da interface de linha de comando.

Isso permitirá que outras interfaces sejam adicionadas posteriormente sem reimplementar o parser.

```text
                 ┌───────────────┐
                 │      CLI      │
                 └───────┬───────┘
                         │
                  ┌──────▼──────┐
                  │ Gaige Core  │
                  └──────┬──────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   Save Parser      Save Writer     Proton Finder
        │                │                │
   Protobuf /        Validação e      Saves Steam
   compressão          backup
```

No futuro:

```text
CLI
 │
 ├── Terminal
 │
 ├── GUI Desktop
 │
 └── outras integrações
 │
 ▼
GaigeSaveEditor Core
```

## Roadmap

O primeiro marco do projeto será propositalmente pequeno.

**v0.1 — Leitura dos saves**

Localizar os saves do Borderlands 2 e extrair informações básicas dos personagens.

**v0.2 — Edição segura**

Backup automático e alteração de nível/experiência.

**v0.3 — Recursos**

Dinheiro, Eridium e outros recursos do personagem.

**v0.4 — Inventário**

Leitura e modificação de armas e itens.

**v0.5 — Protótipo da GUI**

Interface gráfica opcional utilizando o mesmo núcleo Python.

## Inspiração e trabalhos anteriores

O GaigeSaveEditor não pretende ignorar o trabalho já realizado pela comunidade de Borderlands.

Projetos open-source existentes fornecem informações importantes sobre o formato dos saves de Borderlands 2 e poderão servir como referências para o desenvolvimento e validação desta implementação.

Entre eles:

* Gibbed's Borderlands 2 Save Editor
* Pesquisas da comunidade sobre o formato dos saves de Borderlands
* Implementações e experimentos anteriores em Python

Quando código for reutilizado ou adaptado, deverão ser respeitadas as respectivas licenças e exigências de atribuição.

O objetivo é desenvolver uma implementação moderna, reconhecendo adequadamente os trabalhos anteriores.

## Contribuindo

O projeto encontra-se atualmente em estágio experimental.

Contribuições, testes, melhorias na documentação e pesquisas sobre o formato dos saves do Borderlands 2 serão bem-vindos após o estabelecimento da arquitetura básica.

## Aviso legal

GaigeSaveEditor é um projeto comunitário não oficial.

O projeto não possui afiliação, aprovação ou patrocínio da Gearbox Software, 2K Games, Take-Two Interactive ou Valve.

Borderlands, Borderlands 2 e nomes e marcas relacionados pertencem aos seus respectivos proprietários.

Utilize o software por sua conta e risco e mantenha sempre backups dos seus arquivos de save.


## Instalação e desenvolvimento com `pyproject.toml`

O GaigeSaveEditor utiliza o arquivo `pyproject.toml` como principal configuração do projeto Python.

Esse arquivo define os metadados do projeto, versões do Python suportadas, dependências de execução, dependências de desenvolvimento, comandos da CLI e configurações das ferramentas utilizadas.

Isso significa que, para o desenvolvimento normal do projeto, não é necessário manter obrigatoriamente um arquivo `requirements.txt` separado.

### Criar o ambiente virtual

A partir da raiz do projeto:

```bash
python -m venv .venv
```

Ative o ambiente:

```bash
source .venv/bin/activate
```

No Windows:

```powershell
.venv\Scripts\activate
```

### Atualizar o pip

Antes da instalação, é recomendável atualizar o `pip`:

```bash
python -m pip install --upgrade pip
```

### Instalar o GaigeSaveEditor

Para instalar o projeto e suas dependências de execução:

```bash
pip install .
```

Esse comando lê as dependências declaradas em:

```toml
[project]
dependencies = [
    ...
]
```

dentro do `pyproject.toml`.

### Instalar em modo editável

Durante o desenvolvimento, a forma recomendada de instalação é:

```bash
pip install -e .
```

A opção `-e` significa **editable installation**, ou instalação editável.

Nesse modo, alterações realizadas no código-fonte ficam disponíveis imediatamente, sem ser necessário reinstalar o projeto depois de cada modificação.

Por exemplo, depois de alterar:

```text
src/gaige/cli.py
```

o código atualizado já será utilizado ao executar:

```bash
gaige
```

### Instalar dependências de desenvolvimento

O GaigeSaveEditor define ferramentas adicionais de desenvolvimento em:

```toml
[project.optional-dependencies]
dev = [
    ...
]
```

Para instalar o projeto junto com essas dependências:

```bash
pip install -e ".[dev]"
```

Esse é o comando recomendado para desenvolvimento local e para contribuidores.

Ele instala:

* GaigeSaveEditor
* Dependências de execução
* Dependências de testes
* Ferramentas de lint e desenvolvimento

### Verificar a instalação

Após a instalação:

```bash
gaige --help
```

deverá apresentar os comandos disponíveis.

A versão instalada poderá ser consultada com:

```bash
gaige version
```

### Executar os testes

A suíte de testes utiliza `pytest`.

Para executar todos os testes:

```bash
pytest
```

Para uma saída mais detalhada:

```bash
pytest -v
```

Para executar apenas um arquivo de testes:

```bash
pytest tests/test_proton.py
```

Para executar somente um teste específico:

```bash
pytest tests/test_proton.py::test_find_proton_prefix
```

### Cobertura de testes

Caso `pytest-cov` esteja instalado:

```bash
pytest --cov=gaige
```

Para mostrar também quais linhas não estão cobertas:

```bash
pytest --cov=gaige --cov-report=term-missing
```

### Verificação de qualidade do código

O GaigeSaveEditor utiliza Ruff para verificações de qualidade e estilo.

Execute:

```bash
ruff check .
```

Alguns problemas podem ser corrigidos automaticamente:

```bash
ruff check . --fix
```

### Formatação do código

Caso o formatador do Ruff esteja habilitado no projeto:

```bash
ruff format .
```

Para apenas verificar a formatação, sem modificar os arquivos:

```bash
ruff format --check .
```

### Gerar o pacote

O GaigeSaveEditor também poderá ser construído como um pacote Python convencional.

Primeiro, instale o pacote `build`, caso necessário:

```bash
pip install build
```

Depois execute:

```bash
python -m build
```

Os arquivos gerados ficarão no diretório:

```text
dist/
```

Normalmente:

```text
dist/
├── gaige_save_editor-0.1.0-py3-none-any.whl
└── gaige_save_editor-0.1.0.tar.gz
```

### Instalar o pacote gerado

O arquivo Wheel poderá ser instalado diretamente:

```bash
pip install dist/gaige_save_editor-0.1.0-py3-none-any.whl
```

Esse teste é útil porque se aproxima mais do modo como um usuário final receberia o projeto.

### Desinstalar

Para remover o GaigeSaveEditor do ambiente Python atual:

```bash
pip uninstall gaige-save-editor
```

### Fluxo recomendado de desenvolvimento

Uma configuração típica do ambiente será:

```bash
git clone <repository-url>
cd GaigeSaveEditor

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -e ".[dev]"

gaige --help
pytest
ruff check .
```

Depois desses passos, o ambiente estará pronto para o desenvolvimento.

### Comandos úteis do `pip`

Mostrar informações sobre o pacote instalado:

```bash
pip show gaige-save-editor
```

Listar os pacotes instalados:

```bash
pip list
```

Verificar conflitos entre dependências:

```bash
pip check
```

Forçar a reinstalação do projeto:

```bash
pip install --force-reinstall .
```

Durante o desenvolvimento, porém, prefira:

```bash
pip install -e ".[dev]"
```

porque o modo editável evita reinstalações desnecessárias.