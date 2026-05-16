<p align="center">
  <a href="https://2M_CODE.ai">
    <picture>
      <source srcset="packages/console/app/src/asset/logo-ornate-dark.svg" media="(prefers-color-scheme: dark)">
      <source srcset="packages/console/app/src/asset/logo-ornate-light.svg" media="(prefers-color-scheme: light)">
      <img src="packages/console/app/src/asset/logo-ornate-light.svg" alt="2M_CODE logo">
    </picture>
  </a>
</p>
<p align="center">Ο πράκτορας τεχνητής νοημοσύνης ανοικτού κώδικα για προγραμματισμό.</p>
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

### Εγκατάσταση

```bash
# YOLO
curl -fsSL https://2M_CODE.ai/install | bash

# Διαχειριστές πακέτων
npm i -g 2M_CODE-ai@latest        # ή bun/pnpm/yarn
scoop install 2M_CODE             # Windows
choco install 2M_CODE             # Windows
brew install anomalyco/tap/2M_CODE # macOS και Linux (προτείνεται, πάντα ενημερωμένο)
brew install 2M_CODE              # macOS και Linux (επίσημος τύπος brew, λιγότερο συχνές ενημερώσεις)
sudo pacman -S 2M_CODE            # Arch Linux (Σταθερό)
paru -S 2M_CODE-bin               # Arch Linux (Τελευταία έκδοση από AUR)
mise use -g 2M_CODE               # Οποιοδήποτε λειτουργικό σύστημα
nix run nixpkgs#2M_CODE           # ή github:anomalyco/2M_CODE με βάση την πιο πρόσφατη αλλαγή από το dev branch
```

> [!TIP]
> Αφαίρεσε παλαιότερες εκδόσεις από τη 0.1.x πριν από την εγκατάσταση.

### Εφαρμογή Desktop (BETA)

Το 2M_CODE είναι επίσης διαθέσιμο ως εφαρμογή. Κατέβασε το απευθείας από τη [σελίδα εκδόσεων](https://github.com/ArafatAhmed-2M/2mcode/releases) ή το [2M_CODE.ai/download](https://2M_CODE.ai/download).

| Πλατφόρμα             | Λήψη                               |
| --------------------- | ---------------------------------- |
| macOS (Apple Silicon) | `2M_CODE-desktop-mac-arm64.dmg`   |
| macOS (Intel)         | `2M_CODE-desktop-mac-x64.dmg`     |
| Windows               | `2M_CODE-desktop-windows-x64.exe` |
| Linux                 | `.deb`, `.rpm`, ή AppImage         |

```bash
# macOS (Homebrew)
brew install --cask 2M_CODE-desktop
# Windows (Scoop)
scoop bucket add extras; scoop install extras/2M_CODE-desktop
```

#### Κατάλογος Εγκατάστασης

Το script εγκατάστασης τηρεί την ακόλουθη σειρά προτεραιότητας για τη διαδρομή εγκατάστασης:

1. `$2M_CODE_INSTALL_DIR` - Προσαρμοσμένος κατάλογος εγκατάστασης
2. `$XDG_BIN_DIR` - Διαδρομή συμβατή με τις προδιαγραφές XDG Base Directory
3. `$HOME/bin` - Τυπικός κατάλογος εκτελέσιμων αρχείων χρήστη (εάν υπάρχει ή μπορεί να δημιουργηθεί)
4. `$HOME/.2M_CODE/bin` - Προεπιλεγμένη εφεδρική διαδρομή

```bash
# Παραδείγματα
2M_CODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://2M_CODE.ai/install | bash
XDG_BIN_DIR=$HOME/.local/bin curl -fsSL https://2M_CODE.ai/install | bash
```

### Πράκτορες

Το 2M_CODE περιλαμβάνει δύο ενσωματωμένους πράκτορες μεταξύ των οποίων μπορείτε να εναλλάσσεστε με το πλήκτρο `Tab`.

- **build** - Προεπιλεγμένος πράκτορας με πλήρη πρόσβαση για εργασία πάνω σε κώδικα
- **plan** - Πράκτορας μόνο ανάγνωσης για ανάλυση και εξερεύνηση κώδικα
  - Αρνείται την επεξεργασία αρχείων από προεπιλογή
  - Ζητά άδεια πριν εκτελέσει εντολές bash
  - Ιδανικός για εξερεύνηση άγνωστων αρχείων πηγαίου κώδικα ή σχεδιασμό αλλαγών

Περιλαμβάνεται επίσης ένας **general** υποπράκτορας για σύνθετες αναζητήσεις και πολυβηματικές διεργασίες.
Χρησιμοποιείται εσωτερικά και μπορεί να κληθεί χρησιμοποιώντας `@general` στα μηνύματα.

Μάθετε περισσότερα για τους [πράκτορες](https://2M_CODE.ai/docs/agents).

### Οδηγός Χρήσης

Για περισσότερες πληροφορίες σχετικά με τη ρύθμιση του 2M_CODE, [**πλοηγήσου στον οδηγό χρήσης μας**](https://2M_CODE.ai/docs).

### Συνεισφορά

Εάν ενδιαφέρεσαι να συνεισφέρεις στο 2M_CODE, διαβάστε τα [οδηγό χρήσης συνεισφοράς](./CONTRIBUTING.md) πριν υποβάλεις ένα pull request.

### Δημιουργία πάνω στο 2M_CODE

Εάν εργάζεσαι σε ένα έργο σχετικό με το 2M_CODE και χρησιμοποιείτε το "2M_CODE" ως μέρος του ονόματός του, για παράδειγμα "2M_CODE-dashboard" ή "2M_CODE-mobile", πρόσθεσε μια σημείωση στο README σας για να διευκρινίσεις ότι δεν είναι κατασκευασμένο από την ομάδα του 2M_CODE και δεν έχει καμία σχέση με εμάς.

### Συχνές Ερωτήσεις

#### Πώς διαφέρει αυτό από το Claude Code;

Είναι πολύ παρόμοιο με το Claude Code ως προς τις δυνατότητες. Ακολουθούν οι βασικές διαφορές:

- 100% ανοιχτού κώδικα
- Δεν είναι συνδεδεμένο με κανέναν πάροχο. Αν και συνιστούμε τα μοντέλα που παρέχουμε μέσω του [2M_CODE Zen](https://2M_CODE.ai/zen), το 2M_CODE μπορεί να χρησιμοποιηθεί με Claude, OpenAI, Google, ή ακόμα και τοπικά μοντέλα. Καθώς τα μοντέλα εξελίσσονται, τα κενά μεταξύ τους θα κλείσουν και οι τιμές θα μειωθούν, οπότε είναι σημαντικό να είσαι ανεξάρτητος από τον πάροχο.
- Out-of-the-box υποστήριξη LSP
- Εστίαση στο TUI. Το 2M_CODE είναι κατασκευασμένο από χρήστες που χρησιμοποιούν neovim και τους δημιουργούς του [terminal.shop](https://terminal.shop)· θα εξαντλήσουμε τα όρια του τι είναι δυνατό στο terminal.
- Αρχιτεκτονική client/server. Αυτό, για παράδειγμα, μπορεί να επιτρέψει στο 2M_CODE να τρέχει στον υπολογιστή σου ενώ το χειρίζεσαι εξ αποστάσεως από μια εφαρμογή κινητού, που σημαίνει ότι το TUI frontend είναι μόνο ένας από τους πιθανούς clients.

---

**Γίνε μέλος της κοινότητάς μας** [Discord](https://discord.gg/2M_CODE) | [X.com](https://x.com/2M_CODE)
