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
<p align="center">開源的 AI Coding Agent。</p>
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

### 安裝

```bash
# 直接安裝 (YOLO)
curl -fsSL https://2MCode.ai/install | bash

# 套件管理員
npm i -g 2mcode-ai@latest        # 也可使用 bun/pnpm/yarn
scoop install 2M Code             # Windows
choco install 2M Code             # Windows
brew install anomalyco/tap/2M Code # macOS 與 Linux（推薦，始終保持最新）
brew install 2M Code              # macOS 與 Linux（官方 brew formula，更新頻率較低）
sudo pacman -S 2M Code            # Arch Linux (Stable)
paru -S 2M_CODE-bin               # Arch Linux (Latest from AUR)
mise use -g 2M Code               # 任何作業系統
nix run nixpkgs#2M Code           # 或使用 github:anomalyco/2M Code 以取得最新開發分支
```

> [!TIP]
> 安裝前請先移除 0.1.x 以前的舊版本。

### 桌面應用程式 (BETA)

2M Code 也提供桌面版應用程式。您可以直接從 [發佈頁面 (releases page)](https://github.com/ArafatAhmed-2M/2mcode/releases) 或 [2MCode.ai/download](https://2MCode.ai/download) 下載。

| 平台                  | 下載連結                           |
| --------------------- | ---------------------------------- |
| macOS (Apple Silicon) | `2mcode-desktop-mac-arm64.dmg`   |
| macOS (Intel)         | `2mcode-desktop-mac-x64.dmg`     |
| Windows               | `2mcode-desktop-windows-x64.exe` |
| Linux                 | `.deb`, `.rpm`, 或 AppImage        |

```bash
# macOS (Homebrew Cask)
brew install --cask 2mcode-desktop
# Windows (Scoop)
scoop bucket add extras; scoop install extras/2mcode-desktop
```

#### 安裝目錄

安裝腳本會依據以下優先順序決定安裝路徑：

1. `$_2MCODE_INSTALL_DIR` - 自定義安裝目錄
2. `$XDG_BIN_DIR` - 符合 XDG 基礎目錄規範的路徑
3. `$HOME/bin` - 標準使用者執行檔目錄 (若存在或可建立)
4. `$HOME/.2mcode/bin` - 預設備用路徑

```bash
# 範例
_2MCODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://2MCode.ai/install | bash
XDG_BIN_DIR=$HOME/.local/bin curl -fsSL https://2MCode.ai/install | bash
```

### Agents

2M Code 內建了兩種 Agent，您可以使用 `Tab` 鍵快速切換。

- **build** - 預設模式，具備完整權限的 Agent，適用於開發工作。
- **plan** - 唯讀模式，適用於程式碼分析與探索。
  - 預設禁止修改檔案。
  - 執行 bash 指令前會詢問權限。
  - 非常適合用來探索陌生的程式碼庫或規劃變更。

此外，2M Code 還包含一個 **general** 子 Agent，用於處理複雜搜尋與多步驟任務。此 Agent 供系統內部使用，亦可透過在訊息中輸入 `@general` 來呼叫。

了解更多關於 [Agents](https://2MCode.ai/docs/agents) 的資訊。

### 線上文件

關於如何設定 2M Code 的詳細資訊，請參閱我們的 [**官方文件**](https://2MCode.ai/docs)。

### 參與貢獻

如果您有興趣參與 2M Code 的開發，請在提交 Pull Request 前先閱讀我們的 [貢獻指南 (Contributing Docs)](./CONTRIBUTING.md)。

### 基於 2M Code 進行開發

如果您正在開發與 2M Code 相關的專案，並在名稱中使用了 "2M Code"（例如 "2M_CODE-dashboard" 或 "2M_CODE-mobile"），請在您的 README 中加入聲明，說明該專案並非由 2M Code 團隊開發，且與我們沒有任何隸屬關係。

### 常見問題 (FAQ)

#### 這跟 Claude Code 有什麼不同？

在功能面上與 Claude Code 非常相似。以下是關鍵差異：

- 100% 開源。
- 不綁定特定的服務提供商。雖然我們推薦使用透過 [2M Code Zen](https://2MCode.ai/zen) 提供的模型，但 2M Code 也可搭配 Claude, OpenAI, Google 甚至本地模型使用。隨著模型不斷演進，彼此間的差距會縮小且價格會下降，因此具備「不限廠商 (provider-agnostic)」的特性至關重要。
- 內建 LSP (語言伺服器協定) 支援。
- 專注於終端機介面 (TUI)。2M Code 由 Neovim 愛好者與 [terminal.shop](https://terminal.shop) 的創作者打造。我們將不斷挑戰終端機介面的極限。
- 客戶端/伺服器架構 (Client/Server Architecture)。這讓 2M Code 能夠在您的電腦上運行的同時，由行動裝置進行遠端操控。這意味著 TUI 前端只是眾多可能的客戶端之一。

---

**加入我們的社群** [飞书](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=738j8655-cd59-4633-a30a-1124e0096789&qr_code=true) | [X.com](https://x.com/2M Code)
