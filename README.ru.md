<p align="center">
  <a href="https://2M_CODE.ai">
    <picture>
      <source srcset="packages/console/app/src/asset/logo-ornate-dark.svg" media="(prefers-color-scheme: dark)">
      <source srcset="packages/console/app/src/asset/logo-ornate-light.svg" media="(prefers-color-scheme: light)">
      <img src="packages/console/app/src/asset/logo-ornate-light.svg" alt="2M_CODE logo">
    </picture>
  </a>
</p>
<p align="center">Открытый AI-агент для программирования.</p>
<p align="center">
  <a href="https://2M_CODE.ai/discord"><img alt="Discord" src="https://img.shields.io/discord/1391832426048651334?style=flat-square&label=discord" /></a>
  <a href="https://www.npmjs.com/package/2M_CODE-ai"><img alt="npm" src="https://img.shields.io/npm/v/2M_CODE-ai?style=flat-square" /></a>
  <a href="https://github.com/ArafatAhmed-2M/2mcode/actions/workflows/publish.yml"><img alt="Build status" src="https://img.shields.io/github/actions/workflow/status/anomalyco/2M_CODE/publish.yml?style=flat-square&branch=dev" /></a>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh.md">简体中文</a> |
  <a href="README.zht.md">繁體中文</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.it.md">Italiano</a> |
  <a href="README.da.md">Dansk</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.pl.md">Polski</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.bs.md">Bosanski</a> |
  <a href="README.ar.md">العربية</a> |
  <a href="README.no.md">Norsk</a> |
  <a href="README.br.md">Português (Brasil)</a> |
  <a href="README.th.md">ไทย</a> |
  <a href="README.tr.md">Türkçe</a> |
  <a href="README.uk.md">Українська</a> |
  <a href="README.bn.md">বাংলা</a> |
  <a href="README.gr.md">Ελληνικά</a> |
  <a href="README.vi.md">Tiếng Việt</a>
</p>

[![2M_CODE Terminal UI](packages/web/src/assets/lander/screenshot.png)](https://2M_CODE.ai)

---

### Установка

```bash
# YOLO
curl -fsSL https://2M_CODE.ai/install | bash

# Менеджеры пакетов
npm i -g 2M_CODE-ai@latest        # или bun/pnpm/yarn
scoop install 2M_CODE             # Windows
choco install 2M_CODE             # Windows
brew install anomalyco/tap/2M_CODE # macOS и Linux (рекомендуем, всегда актуально)
brew install 2M_CODE              # macOS и Linux (официальная формула brew, обновляется реже)
sudo pacman -S 2M_CODE            # Arch Linux (Stable)
paru -S 2M_CODE-bin               # Arch Linux (Latest from AUR)
mise use -g 2M_CODE               # любая ОС
nix run nixpkgs#2M_CODE           # или github:anomalyco/2M_CODE для самой свежей ветки dev
```

> [!TIP]
> Перед установкой удалите версии старше 0.1.x.

### Десктопное приложение (BETA)

2M_CODE также доступен как десктопное приложение. Скачайте его со [страницы релизов](https://github.com/ArafatAhmed-2M/2mcode/releases) или с [2M_CODE.ai/download](https://2M_CODE.ai/download).

| Платформа             | Загрузка                           |
| --------------------- | ---------------------------------- |
| macOS (Apple Silicon) | `2M_CODE-desktop-mac-arm64.dmg`   |
| macOS (Intel)         | `2M_CODE-desktop-mac-x64.dmg`     |
| Windows               | `2M_CODE-desktop-windows-x64.exe` |
| Linux                 | `.deb`, `.rpm` или AppImage        |

```bash
# macOS (Homebrew)
brew install --cask 2M_CODE-desktop
# Windows (Scoop)
scoop bucket add extras; scoop install extras/2M_CODE-desktop
```

#### Каталог установки

Скрипт установки выбирает путь установки в следующем порядке приоритета:

1. `$2M_CODE_INSTALL_DIR` - Пользовательский каталог установки
2. `$XDG_BIN_DIR` - Путь, совместимый со спецификацией XDG Base Directory
3. `$HOME/bin` - Стандартный каталог пользовательских бинарников (если существует или можно создать)
4. `$HOME/.2M_CODE/bin` - Fallback по умолчанию

```bash
# Примеры
2M_CODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://2M_CODE.ai/install | bash
XDG_BIN_DIR=$HOME/.local/bin curl -fsSL https://2M_CODE.ai/install | bash
```

### Agents

В 2M_CODE есть два встроенных агента, между которыми можно переключаться клавишей `Tab`.

- **build** - По умолчанию, агент с полным доступом для разработки
- **plan** - Агент только для чтения для анализа и изучения кода
  - По умолчанию запрещает редактирование файлов
  - Запрашивает разрешение перед выполнением bash-команд
  - Идеален для изучения незнакомых кодовых баз или планирования изменений

Также включен сабагент **general** для сложных поисков и многошаговых задач.
Он используется внутренне и может быть вызван в сообщениях через `@general`.

Подробнее об [agents](https://2M_CODE.ai/docs/agents).

### Документация

Больше информации о том, как настроить 2M_CODE: [**наши docs**](https://2M_CODE.ai/docs).

### Вклад

Если вы хотите внести вклад в 2M_CODE, прочитайте [contributing docs](./CONTRIBUTING.md) перед тем, как отправлять pull request.

### Разработка на базе 2M_CODE

Если вы делаете проект, связанный с 2M_CODE, и используете "2M_CODE" как часть имени (например, "2M_CODE-dashboard" или "2M_CODE-mobile"), добавьте примечание в README, чтобы уточнить, что проект не создан командой 2M_CODE и не аффилирован с нами.

### FAQ

#### Чем это отличается от Claude Code?

По возможностям это очень похоже на Claude Code. Вот ключевые отличия:

- 100% open source
- Не привязано к одному провайдеру. Мы рекомендуем модели из [2M_CODE Zen](https://2M_CODE.ai/zen); но 2M_CODE можно использовать с Claude, OpenAI, Google или даже локальными моделями. По мере развития моделей разрыв будет сокращаться, а цены падать, поэтому важна независимость от провайдера.
- Поддержка LSP из коробки
- Фокус на TUI. 2M_CODE построен пользователями neovim и создателями [terminal.shop](https://terminal.shop); мы будем раздвигать границы того, что возможно в терминале.
- Архитектура клиент/сервер. Например, это позволяет запускать 2M_CODE на вашем компьютере, а управлять им удаленно из мобильного приложения. Это значит, что TUI-фронтенд - лишь один из возможных клиентов.

---

**Присоединяйтесь к нашему сообществу** [Discord](https://discord.gg/2M_CODE) | [X.com](https://x.com/2M_CODE)
