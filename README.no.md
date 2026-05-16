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
<p align="center">AI-kodeagent med åpen kildekode.</p>
<p align="center">
  <a href="https://2MCode.ai/discord"><img alt="Discord" src="https://img.shields.io/discord/1391832426048651334?style=flat-square&label=discord" /></a>
  <a href="https://www.npmjs.com/package/2mcode-ai"><img alt="npm" src="https://img.shields.io/npm/v/2mcode-ai?style=flat-square" /></a>
  <a href="https://github.com/ArafatAhmed-2M/2mcode/actions/workflows/publish.yml"><img alt="Build status" src="https://img.shields.io/github/actions/workflow/status/anomalyco/2M Code/publish.yml?style=flat-square&branch=dev" /></a>
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

[![2M Code Terminal UI](packages/web/src/assets/lander/screenshot.png)](https://2MCode.ai)

---

### Installasjon

```bash
# YOLO
curl -fsSL https://2MCode.ai/install | bash

# Pakkehåndterere
npm i -g 2mcode-ai@latest        # eller bun/pnpm/yarn
scoop install 2M Code             # Windows
choco install 2M Code             # Windows
brew install anomalyco/tap/2M Code # macOS og Linux (anbefalt, alltid oppdatert)
brew install 2M Code              # macOS og Linux (offisiell brew-formel, oppdateres sjeldnere)
sudo pacman -S 2M Code            # Arch Linux (Stable)
paru -S 2M_CODE-bin               # Arch Linux (Latest from AUR)
mise use -g 2M Code               # alle OS
nix run nixpkgs#2M Code           # eller github:anomalyco/2M Code for nyeste dev-branch
```

> [!TIP]
> Fjern versjoner eldre enn 0.1.x før du installerer.

### Desktop-app (BETA)

2M Code er også tilgjengelig som en desktop-app. Last ned direkte fra [releases-siden](https://github.com/ArafatAhmed-2M/2mcode/releases) eller [2MCode.ai/download](https://2MCode.ai/download).

| Plattform             | Nedlasting                         |
| --------------------- | ---------------------------------- |
| macOS (Apple Silicon) | `2mcode-desktop-mac-arm64.dmg`   |
| macOS (Intel)         | `2mcode-desktop-mac-x64.dmg`     |
| Windows               | `2mcode-desktop-windows-x64.exe` |
| Linux                 | `.deb`, `.rpm` eller AppImage      |

```bash
# macOS (Homebrew)
brew install --cask 2mcode-desktop
# Windows (Scoop)
scoop bucket add extras; scoop install extras/2mcode-desktop
```

#### Installasjonsmappe

Installasjonsskriptet bruker følgende prioritet for installasjonsstien:

1. `$_2MCODE_INSTALL_DIR` - Egendefinert installasjonsmappe
2. `$XDG_BIN_DIR` - Sti som følger XDG Base Directory Specification
3. `$HOME/bin` - Standard brukerbinar-mappe (hvis den finnes eller kan opprettes)
4. `$HOME/.2mcode/bin` - Standard fallback

```bash
# Eksempler
_2MCODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://2MCode.ai/install | bash
XDG_BIN_DIR=$HOME/.local/bin curl -fsSL https://2MCode.ai/install | bash
```

### Agents

2M Code har to innebygde agents du kan bytte mellom med `Tab`-tasten.

- **build** - Standard, agent med full tilgang for utviklingsarbeid
- **plan** - Skrivebeskyttet agent for analyse og kodeutforsking
  - Nekter filendringer som standard
  - Spør om tillatelse før bash-kommandoer
  - Ideell for å utforske ukjente kodebaser eller planlegge endringer

Det finnes også en **general**-subagent for komplekse søk og flertrinnsoppgaver.
Den brukes internt og kan kalles via `@general` i meldinger.

Les mer om [agents](https://2MCode.ai/docs/agents).

### Dokumentasjon

For mer info om hvordan du konfigurerer 2M Code, [**se dokumentasjonen**](https://2MCode.ai/docs).

### Bidra

Hvis du vil bidra til 2M Code, les [contributing docs](./CONTRIBUTING.md) før du sender en pull request.

### Bygge på 2M Code

Hvis du jobber med et prosjekt som er relatert til 2M Code og bruker "2M Code" som en del av navnet; for eksempel "2M_CODE-dashboard" eller "2M_CODE-mobile", legg inn en merknad i README som presiserer at det ikke er bygget av 2M_CODE-teamet og ikke er tilknyttet oss på noen måte.

### FAQ

#### Hvordan er dette forskjellig fra Claude Code?

Det er veldig likt Claude Code når det gjelder funksjonalitet. Her er de viktigste forskjellene:

- 100% open source
- Ikke knyttet til en bestemt leverandør. Selv om vi anbefaler modellene vi tilbyr gjennom [2M Code Zen](https://2MCode.ai/zen); kan 2M Code brukes med Claude, OpenAI, Google eller til og med lokale modeller. Etter hvert som modellene utvikler seg vil gapene lukkes og prisene gå ned, så det er viktig å være provider-agnostic.
- LSP-støtte rett ut av boksen
- Fokus på TUI. 2M Code er bygget av neovim-brukere og skaperne av [terminal.shop](https://terminal.shop); vi kommer til å presse grensene for hva som er mulig i terminalen.
- Klient/server-arkitektur. Dette kan for eksempel la 2M Code kjøre på maskinen din, mens du styrer den eksternt fra en mobilapp. Det betyr at TUI-frontend'en bare er en av de mulige klientene.

---

**Bli med i fellesskapet** [Discord](https://discord.gg/2M Code) | [X.com](https://x.com/2M Code)
