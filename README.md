# ✨ Anime Suki ✨
## 💓 A little project to upload cute images 💓

## 🔗 Link: http://anime-suki.online/

## 🛠️ 開發流程：
- 撰寫 local 可運行的程式功能：
  1. main.py：使用 fastapi `Jinja2Templates` 製作 templates。
  2. database.py 設定：使用 `mysql.connector` 的 `pooling` 來處理 DB connection pool，解決過去每次 server 訪問 DB 都要重新建立連線的昂貴問題。
  3. database.py ：使用  [contextmanager](https://docs.python.org/zh-tw/3/library/contextlib.html) 將連線方法以 generator 傳遞，並在 `image_controller` 使用 `with` 處理 DB 訪問結束後的資源釋放。
  4. image_controller：製作 `GET /images`、`POST /image` API。並可透過 API 上傳圖片到本地資料夾。
  5. templates: 製作 `base.html`、`index.html`。
  6. index.js: 渲染 index.html 時 fetch `GETT /images`取得現有圖片，上傳鈕按下後， fetch `POST /image`將文件上傳，並取得 return 的 image url 與 note。

- 設定 AWS 、Godadddy 資源：
  1. 使用 Godaddy 註冊 `anime-suki.online` 網域。
  2. 建立 AWS EC2。
  3. 建立 AWS S3 後，於 `.env` 撰寫環境變數設定。
  4. 建立 AWS RDS 後，於 `.env` 撰寫環境變數設定。
  5. 撰寫 `.env.production` ，區分正式區與 develop 環境設定。
  6. `image_controller` 更改檔案上傳設定，如果`env`是正式區，才上傳 S3。
  7. 撰寫 `Dockerfile`、`requirements.txt`，用於稍晚建立 server container。
  8. 撰寫 `docker-compose.yml`，指定 EC2 port 8000 連線到 container port 8000。

- 正式區設定：
  1. EC2 安裝 git、docker、docker-compose。
  2. 開 CloudFront，更改 `images_controller` 檔案上傳 URL 設定 (加入 distribution domain name)。
  3. git push github 後，至 EC2 git clone github repo。
  4. docker-compose up --build。
  5. Godaddy DNS 設定：將 anime-suki.online 綁定 EC2 的 ip。
  6. 由於目前是 HTTP Request，是訪問 port 80，因此在 EC2 上先設定將HTTP request redirect 到 port 8000。
