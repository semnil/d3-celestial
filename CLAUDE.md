# d3-celestial sky.html 生成仕様

OBS ブラウザソース用 1920×1080 星図背景。`git clone https://github.com/ofrohn/d3-celestial` 直後の状態を起点とする。

## 配置

- `sky.html` をリポジトリルートに新規作成。
- `serve.py` をリポジトリルートに新規作成 (配信スクリプト、純粋な静的配信 + キャッシュ抑止のみ)。
- 既存ファイルは `.gitignore` の追記を除き変更しない。
- スクリプトはルート相対で読み込む:
  - `lib/d3.min.js`
  - `lib/d3.geo.projection.min.js`
  - `celestial.min.js`

## 仕様

| 項目 | 値 |
|---|---|
| ビューポート | 1920×1080、`<body>` 全面、背景 `#2a2e42` (ミッドナイトブルー寄り) |
| 観測地 | sky.html に `LAT` / `LON` (10進度) をハードコード。デフォルトは東京駅丸の内中央口 (35.681236, 139.767125) |
| 時刻 | 実時間 (1 秒間隔で `Celestial.date(new Date())` を呼ぶ。1 時間で天球が約 15° 回転) |
| 右下 | 2 行表示 (右揃え、白文字 12px、line-height 1.4)。1 行目 `Star map: d3-celestial (BSD)`、2 行目 `github.com/ofrohn/d3-celestial` |
| 投影 | stereographic、デフォルトスケール (上書きなし、ratio=1.0 で canvas は 1920×1920) |
| 表示中心 | `#celestial-map` を `transform: translateX(calc(1920px / 8)) scale(1.15)` で 240px 右にオフセット + 1.15 倍拡大 (origin: center) |
| 表示 | 星 / 天の川 (淡め opacity 0.02) / 惑星 (記号 + 3 文字略称 desig) / 星座線 (細め width 0.8) / 星座名 (3 文字略称 desig) / グラティキュール (細線 `#a8b0d4` width 0.3) を表示。星名 / DSO / 赤道線 / 黄道線 / 星座境界は非表示 |
| UI | controls / formFields / advanced すべて非表示 |

## DOM

```html
<body>
  <div id="marker">Star map: d3-celestial (BSD)<br>github.com/ofrohn/d3-celestial</div>
  <div id="celestial-map"></div>
</body>
```

## CSS

- `html, body { margin:0; padding:0; background:#2a2e42; overflow:hidden; }`
- `#celestial-map { width:1920px; height:1080px; transform: translateX(calc(1920px / 8)) scale(1.15); transform-origin: center center; }`
- `#marker { position:fixed; bottom:16px; right:16px; color:#fff; font:bold 12px sans-serif; text-align:right; line-height:1.4; z-index:10; }`

## d3-celestial config

`demo/sky.html` の config を参照しつつ、以下で生成する:

```js
const LAT = 35.681236; // 東京駅丸の内中央口
const LON = 139.767125;

const config = {
  width: 1920,
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

setInterval(() => Celestial.date(new Date()), 1000);
```

## 起動

1. 観測地を変更したい場合は `sky.html` の `LAT` / `LON` を直接編集。
2. `./serve.py` (または `python3 serve.py`) で配信。`PORT` 環境変数で待受ポート変更可能 (デフォルト 8080)。

## 検証

1. ルートで `./serve.py`
2. `http://localhost:8080/sky.html` を開いて確認:
   - ミッドナイトブルー背景 (`#2a2e42`) に星・天の川 (淡め)・惑星 (記号 + 3 文字略称: Mer / Ven / Mar / Jup / Sat / Ura / Nep / Sol / Lun など)・星座線・星座名 (3 文字略称: UMa / Ori / Cas など)・グラティキュール (細線 `#a8b0d4`) が描画されている。星名・DSO・赤道線・黄道線・星座境界は非表示
   - 天球の中心が画面中央から右へ 1/8 (240px) オフセット、全体 1.15 倍拡大 (`#celestial-map` の CSS `transform: translateX ... scale(1.15)`、origin center)
   - 右下に白文字 12px (右揃え、2 行) で 1 行目 `Star map: d3-celestial (BSD)`、2 行目 `github.com/ofrohn/d3-celestial`
   - フォーム・コントロール類は表示されていない
   - 天球は実時間で進行 (1 時間で約 15° 回転)
3. OBS ブラウザソース 1920×1080 で同 URL を読ませて同等の表示になること
