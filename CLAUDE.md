# d3-celestial sky.html / sky-full.html 生成仕様

OBS ブラウザソース 1920×1080 を主用途とした星図ページを 2 バリアント生成する。`git clone https://github.com/ofrohn/d3-celestial` 直後の状態を起点とし、既存ファイルは `.gitignore` 追記を除き変更しない。

## バリアント

| 用途 | ファイル | 概要 |
|---|---|---|
| OBS 配信背景 (運用中) | `sky.html` | 1920×1920 canvas を上下クロップして 1080 高さに収め、画面中央から 240px 右へオフセット + 1.15 倍拡大、実時間で天球が回転 |
| 全天可視のスタンドアロン表示 | `sky-full.html` | 1080×1080 canvas (全天円が画面高さ内に完全収まる) を 1920 幅ビューポートの水平中央に配置、読込時刻で静止 |

両者は以下の差分以外完全に同一 (DOM・観測地・マーカー・celestial config の他フィールド・読み込むスクリプトすべて共通)。

| 項目 | sky.html | sky-full.html |
|---|---|---|
| `config.width` | `1920` | `1080` |
| canvas 実サイズ | 1920×1920 (上下計 840px が viewport 外で切れる) | 1080×1080 (全円表示) |
| `#celestial-map` CSS | `width:1920px; height:1080px; transform: translateX(calc(1920px / 8)) scale(1.15); transform-origin: center center;` | `width:1080px; height:1080px; margin:0 auto;` |
| 時刻更新 | `setInterval(() => Celestial.date(new Date()), 1000)` (1 時間で約 15° 回転) | なし (`new Date()` を `config.datetime` に渡したまま静止) |

## 配置

- `sky.html` / `sky-full.html` をリポジトリルートに新規作成。
- `serve.py` をリポジトリルートに新規作成 (純粋な静的配信 + キャッシュ抑止のみ)。
- スクリプトはルート相対で読み込む:
  - `lib/d3.min.js`
  - `lib/d3.geo.projection.min.js`
  - `celestial.min.js`

## 共通仕様

| 項目 | 値 |
|---|---|
| ビューポート | 1920×1080、`<body>` 全面、背景 `#2a2e42` (ミッドナイトブルー寄り) |
| 観測地 | `LAT` / `LON` (10進度) を各 html にハードコード。デフォルトは東京駅丸の内中央口 (35.681236, 139.767125)。両ファイル同期して編集 |
| 投影 | stereographic、デフォルトスケール (上書きなし、ratio=1.0 で canvas は `config.width × config.width`) |
| 右下マーカー | 2 行表示 (右揃え、白文字 12px、line-height 1.4)。1 行目 `Star map: d3-celestial (BSD)`、2 行目 `github.com/ofrohn/d3-celestial` |
| 表示要素 | 星 / 天の川 (淡め opacity 0.02) / 惑星 (記号 + 3 文字略称 desig) / 星座線 (細め width 0.8) / 星座名 (3 文字略称 desig) / グラティキュール (細線 `#a8b0d4` width 0.3)。星名 / DSO / 赤道線 / 黄道線 / 星座境界は非表示 |
| UI | controls / formFields / advanced すべて非表示 |

## DOM (両ファイル共通)

```html
<body>
  <div id="marker">Star map: d3-celestial (BSD)<br>github.com/ofrohn/d3-celestial</div>
  <div id="celestial-map"></div>
</body>
```

## CSS

共通:

```css
html, body { margin:0; padding:0; background:#2a2e42; overflow:hidden; }
#marker { position:fixed; bottom:16px; right:16px; color:#fff; font:bold 12px sans-serif; text-align:right; line-height:1.4; z-index:10; }
```

`#celestial-map` だけがバリアント間で異なる (上記差分テーブル参照)。

## d3-celestial config

`demo/sky.html` の config を参照しつつ、以下で生成する (`width` のみバリアント差分、その他は共通):

```js
const LAT = 35.681236; // 東京駅丸の内中央口
const LON = 139.767125;

const config = {
  width: 1920, // sky.html: 1920、sky-full.html: 1080
  projection: "stereographic",
  transform: "equatorial",
  geopos: [LAT, LON],
  location: true, // 観測地ベース計算を有効化。これがないと惑星描画ブロック (celestial.js:595) が全スキップされる
  follow: "zenith",
  controls: false,
  advanced: false,
  formFields: { location: false, date: false, controls: false },
  background: { fill: "#2a2e42", stroke: "#2a2e42", opacity: 1 },
  stars: { show: true, limit: 6, colors: true, size: 7, designation: false },
  constellations: { names: true, namesType: "desig", lines: true, bounds: false, lineStyle: { stroke: "#cccccc", width: 0.8, opacity: 0.6 } }, // show は明示しない (true 指定時 names が強制 true 化される celestial の互換挙動を回避)。lineStyle は shallow 上書きされるため stroke/opacity もデフォルト値を再指定
  mw: { show: true, style: { fill: "#ffffff", opacity: 0.02 } },
  planets: { show: true, symbolType: "disk", names: true, namesType: "desig" },
  dsos: { show: false, names: false },
  lines: {
    graticule: { show: true, stroke: "#a8b0d4", width: 0.3 },
    equatorial: { show: false },
    ecliptic: { show: false },
  },
  horizon: { show: true, stroke: "#2a2e42", fill: "#2a2e42", opacity: 1 },
  datetime: new Date(),
};

Celestial.display(config);

// sky.html のみ
setInterval(() => Celestial.date(new Date()), 1000);
```

## 起動

OBS ブラウザソースまたはブラウザに渡す URL:

- **GitHub Pages (推奨、運用中)**: `https://semnil.github.io/d3-celestial/{sky,sky-full}.html`
  - `obs-sky` ブランチの root を Pages のソースに設定済み。`git push` で数十秒〜数分後に反映
  - 初回ロード ~1.2MB (data/*.json fetch)、以後は GitHub Pages の `Cache-Control` で 10 分キャッシュ
- **ローカル配信**: `./serve.py` (または `python3 serve.py`) を起動し `http://localhost:8080/{sky,sky-full}.html` を指定。`PORT` 環境変数で待受ポート変更可能 (デフォルト 8080)
- 観測地を変更したい場合は両ファイルの `LAT` / `LON` を同期して編集してから push / 起動

## 検証

両ファイルを順に開き、以下を確認:

1. **共通**: ミッドナイトブルー背景 (`#2a2e42`) に星・天の川 (淡め)・惑星 (記号 + 3 文字略称: Mer / Ven / Mar / Jup / Sat / Ura / Nep / Sol / Lun など)・星座線・星座名 (3 文字略称: UMa / Ori / Cas など)・グラティキュール (細線 `#a8b0d4`) が描画され、星名・DSO・赤道線・黄道線・星座境界は非表示。右下に白文字 12px の 2 行マーカー。フォーム・コントロール類は非表示。
2. **`sky.html` 固有**: 天球の中心が画面中央から右へ 1/8 (240px) オフセット、全体 1.15 倍拡大。天球は実時間で進行 (1 時間で約 15° 回転)。
3. **`sky-full.html` 固有**: 天球の全円 (直径 1080) が画面高さ内に完全収まる。canvas (1080×1080) は 1920 幅ビューポートの水平中央に配置され、左右に 420px ずつのミッドナイトブルー余白。天球は読込時刻で静止 (時間が進んでも回転しない)。
4. OBS ブラウザソース 1920×1080 で各 URL を読ませて同等の表示になること。
