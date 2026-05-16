<p align="center">

`	ext
██████╗ ███╗   ███╗     ██████╗ ██████╗ ██████╗ ███████╗
╚════██╗████╗ ████║    ██╔════╝██╔═══██╗██╔══██╗██╔════╝
 █████╔╝██╔████╔██║    ██║     ██║   ██║██║  ██║█████╗  
██╔═══╝ ██║╚██╔╝██║    ██║     ██║   ██║██║  ██║██╔══╝  
███████╗██║ ╚═╝ ██║    ╚██████╗╚██████╔╝██████╔╝███████╗
╚══════╝╚═╝     ╚═╝     ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
`

</p>
<p align="center">El agente de programación con IA de código abierto.</p>
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

### Instalación

```bash
# YOLO
curl -fsSL https://2M_CODE.ai/install | bash

# Gestores de paquetes
npm i -g 2M_CODE-ai@latest        # o bun/pnpm/yarn
scoop install 2M_CODE             # Windows
choco install 2M_CODE             # Windows
brew install anomalyco/tap/2M_CODE # macOS y Linux (recomendado, siempre al día)
brew install 2M_CODE              # macOS y Linux (fórmula oficial de brew, se actualiza menos)
sudo pacman -S 2M_CODE            # Arch Linux (Stable)
paru -S 2M_CODE-bin               # Arch Linux (Latest from AUR)
mise use -g 2M_CODE               # cualquier sistema
nix run nixpkgs#2M_CODE           # o github:anomalyco/2M_CODE para la rama dev más reciente
```

> [!TIP]
> Elimina versiones anteriores a 0.1.x antes de instalar.

### App de escritorio (BETA)

2M_CODE también está disponible como aplicación de escritorio. Descárgala directamente desde la [página de releases](https://github.com/ArafatAhmed-2M/2mcode/releases) o desde [2M_CODE.ai/download](https://2M_CODE.ai/download).

| Plataforma            | Descarga                           |
| --------------------- | ---------------------------------- |
| macOS (Apple Silicon) | `2M_CODE-desktop-mac-arm64.dmg`   |
| macOS (Intel)         | `2M_CODE-desktop-mac-x64.dmg`     |
| Windows               | `2M_CODE-desktop-windows-x64.exe` |
| Linux                 | `.deb`, `.rpm`, o AppImage         |

```bash
# macOS (Homebrew)
brew install --cask 2M_CODE-desktop
# Windows (Scoop)
scoop bucket add extras; scoop install extras/2M_CODE-desktop
```

#### Directorio de instalación

El script de instalación respeta el siguiente orden de prioridad para la ruta de instalación:

1. `$2M_CODE_INSTALL_DIR` - Directorio de instalación personalizado
2. `$XDG_BIN_DIR` - Ruta compatible con la especificación XDG Base Directory
3. `$HOME/bin` - Directorio binario estándar del usuario (si existe o se puede crear)
4. `$HOME/.2M_CODE/bin` - Alternativa por defecto

```bash
# Ejemplos
2M_CODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://2M_CODE.ai/install | bash
XDG_BIN_DIR=$HOME/.local/bin curl -fsSL https://2M_CODE.ai/install | bash
```

### Agents

2M_CODE incluye dos agents integrados que puedes alternar con la tecla `Tab`.

- **build** - Por defecto, agent con acceso completo para trabajo de desarrollo
- **plan** - Agent de solo lectura para análisis y exploración de código
  - Niega ediciones de archivos por defecto
  - Pide permiso antes de ejecutar comandos bash
  - Ideal para explorar codebases desconocidas o planificar cambios

Además, incluye un subagent **general** para búsquedas complejas y tareas de varios pasos.
Se usa internamente y se puede invocar con `@general` en los mensajes.

Más información sobre [agents](https://2M_CODE.ai/docs/agents).

### Documentación

Para más información sobre cómo configurar 2M_CODE, [**ve a nuestra documentación**](https://2M_CODE.ai/docs).

### Contribuir

Si te interesa contribuir a 2M_CODE, lee nuestras [docs de contribución](./CONTRIBUTING.md) antes de enviar un pull request.

### Construyendo sobre 2M_CODE

Si estás trabajando en un proyecto relacionado con 2M_CODE y usas "2M_CODE" como parte del nombre; por ejemplo, "2M_CODE-dashboard" u "2M_CODE-mobile", agrega una nota en tu README para aclarar que no está construido por el equipo de 2M_CODE y que no está afiliado con nosotros de ninguna manera.

### FAQ

#### ¿En qué se diferencia de Claude Code?

Es muy similar a Claude Code en cuanto a capacidades. Estas son las diferencias clave:

- 100% open source
- No está acoplado a ningún proveedor. Aunque recomendamos los modelos que ofrecemos a través de [2M_CODE Zen](https://2M_CODE.ai/zen); 2M_CODE se puede usar con Claude, OpenAI, Google o incluso modelos locales. A medida que evolucionan los modelos, las brechas se cerrarán y los precios bajarán, por lo que ser agnóstico al proveedor es importante.
- Soporte LSP listo para usar
- Un enfoque en la TUI. 2M_CODE está construido por usuarios de neovim y los creadores de [terminal.shop](https://terminal.shop); vamos a empujar los límites de lo que es posible en la terminal.
- Arquitectura cliente/servidor. Esto, por ejemplo, permite ejecutar 2M_CODE en tu computadora mientras lo controlas de forma remota desde una app móvil. Esto significa que el frontend TUI es solo uno de los posibles clientes.

---

**Únete a nuestra comunidad** [Discord](https://discord.gg/2M_CODE) | [X.com](https://x.com/2M_CODE)
