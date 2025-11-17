# ValueCell 部署指南（完全免费）

## 架构概览

- **前端**：Vercel (valuecell.hivince.com) - 免费
- **后端**：Fly.io (Python FastAPI) - 免费套餐
- **数据库**：SQLite（Fly.io 持久化存储）
- **总成本**：$0/月

---

## 1️⃣ 后端部署 (Fly.io)

### 步骤 1：安装 Fly CLI

```bash
# macOS
brew install flyctl

# 或使用安装脚本
curl -L https://fly.io/install.sh | sh
```

### 步骤 2：注册并登录

```bash
# 注册新账号（完全免费）
fly auth signup

# 或登录已有账号
fly auth login
```

### 步骤 3：部署应用

```bash
# 在项目根目录
cd /path/to/valuecell

# 启动部署（使用已有的 fly.toml）
fly launch --no-deploy

# 选择应用名称，如：valuecell-backend
# 选择区域，如：sjc（旧金山）或 nrt（东京）或 hkg（香港）
```

### 步骤 4：配置环境变量（Secrets）

**必需配置**：
```bash
fly secrets set \
  OPENROUTER_API_KEY="your_openrouter_key_here" \
  GOOGLE_API_KEY="your_google_key_here"
```

**可选配置**：
```bash
fly secrets set \
  OPENAI_API_KEY="your_openai_key_here" \
  SILICONFLOW_API_KEY="your_siliconflow_key_here" \
  FINNHUB_API_KEY="your_finnhub_key_here" \
  SEC_EMAIL="your_email@example.com"
```

**交易所配置**（如需自动交易）：
```bash
fly secrets set \
  OKX_NETWORK="paper" \
  OKX_API_KEY="your_okx_key" \
  OKX_API_SECRET="your_okx_secret" \
  OKX_API_PASSPHRASE="your_okx_passphrase" \
  OKX_ALLOW_LIVE_TRADING="false"
```

### 步骤 5：创建持久化存储

```bash
# 创建 1GB 存储卷（免费套餐内）
fly volumes create valuecell_data --size 1
```

### 步骤 6：部署

```bash
fly deploy
```

部署成功后，你会得到一个免费的 URL：
```
https://valuecell-backend.fly.dev
```

记录这个 URL，用于前端配置。

### 步骤 7：验证部署

```bash
# 检查应用状态
fly status

# 查看日志
fly logs

# 测试健康检查
curl https://valuecell-backend.fly.dev/api/v1/health
```

---

## 2️⃣ 前端部署 (Vercel)

### 步骤 1：连接 GitHub 仓库

1. 访问 https://vercel.com/ 并登录
2. 点击 "Add New" → "Project"
3. 导入你的 `valuecell` GitHub 仓库

### 步骤 2：配置项目

**Framework Preset**: Vite
**Root Directory**: `frontend`
**Build Command**: `bun install && bun run build`
**Output Directory**: `build/client`
**Install Command**: `npm install -g bun && bun install`

### 步骤 3：配置环境变量

在 Vercel 项目 → Settings → Environment Variables 中添加：

```bash
VITE_API_BASE_URL=https://valuecell-backend.fly.dev/api/v1
```

**注意**：将 URL 替换为你的 Fly.io 后端实际地址。

### 步骤 4：配置自定义域名

1. 进入 Vercel 项目 → Settings → Domains
2. 添加域名：`valuecell.hivince.com`
3. Vercel 会提供 DNS 配置说明，通常是添加 CNAME 记录：
   ```
   Name: valuecell
   Type: CNAME
   Value: cname.vercel-dns.com
   ```
4. 在你的 DNS 服务商（如 Cloudflare、阿里云等）添加该记录

### 步骤 5：部署

点击 "Deploy"，Vercel 会自动构建并部署前端。

---

## 3️⃣ 验证部署

### 测试后端

访问 Fly.io 后端 URL：
```bash
curl https://valuecell-backend.fly.dev/api/v1/health
```

应该返回：
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

### 测试前端

访问：`https://valuecell.hivince.com`

应该能看到 ValueCell 界面，并且能正常调用后端 API。

---

## 4️⃣ 后续维护

### 更新代码

当你推送代码到 GitHub 的 `main` 分支时：
- **Vercel** 会自动重新构建和部署前端
- **Fly.io** 需要手动部署：
  ```bash
  fly deploy
  ```

### 监控日志

- **Fly.io**：
  ```bash
  fly logs              # 实时日志
  fly status            # 应用状态
  fly ssh console       # SSH 进入容器
  ```
- **Vercel**：项目 → Deployments → 查看构建日志

### 数据库备份

定期备份 Fly.io 上的 `valuecell.db`：
```bash
# 使用 Fly.io SSH
fly ssh console
sqlite3 /data/valuecell.db ".backup /data/backup.db"

# 或下载到本地
fly sftp get /data/valuecell.db valuecell_backup.db
```

### 扩展资源（如果需要）

```bash
# 查看当前资源使用
fly scale show

# 调整内存（免费套餐内）
fly scale memory 512

# 查看计费状态
fly billing show
```

---

## 🎯 API Keys 获取地址汇总

| 服务 | 获取地址 | 说明 |
|------|---------|------|
| OpenRouter | https://openrouter.ai/ | 推荐的主要 LLM 提供商 |
| Google AI | https://aistudio.google.com/ | 免费的嵌入模型 |
| OpenAI | https://platform.openai.com/ | 可选的 LLM 提供商 |
| SiliconFlow | https://siliconflow.cn | 国内友好的 LLM |
| Finnhub | https://finnhub.io/register | 免费金融新闻 API |
| OKX | https://www.okx.com/ | 加密货币交易所 |

---

## 💡 优化建议

### 性能优化

1. **Fly.io**：选择离你最近的区域（香港 hkg、东京 nrt、新加坡 sin）
2. **Vercel**：启用 Edge Functions 加速全球访问
3. **CDN**：使用 Cloudflare 加速静态资源

### 安全建议

1. 启用 HTTPS（Vercel 和 Fly.io 默认支持）
2. 配置 CORS 允许的域名（仅允许 `valuecell.hivince.com`）
3. 定期更新依赖包
4. 不要在代码中硬编码 API keys
5. 使用 `fly secrets` 管理敏感信息

### 成本预估

- **Vercel**: 免费（个人项目）
- **Fly.io**: 免费（免费套餐）
- **总计**: **$0/月** 🎉

#### Fly.io 免费套餐详情：
- 3个共享 CPU 虚拟机
- 3GB 持久化存储
- 每月 160GB 出站流量
- 自动 HTTPS

---

## 🆘 故障排查

### 前端无法连接后端

1. 检查 Vercel 环境变量 `VITE_API_BASE_URL` 是否正确
2. 检查 Fly.io 后端是否正常运行：`fly status`
3. 检查浏览器控制台的网络请求
4. 检查 CORS 配置

### 后端启动失败

1. 查看 Fly.io 日志：`fly logs`
2. 检查 Secrets 是否完整：`fly secrets list`
3. 确认 Docker 构建是否成功
4. SSH 进入容器排查：`fly ssh console`

### 域名无法访问

1. 检查 DNS 记录是否正确配置
2. 等待 DNS 传播（最多 48 小时）
3. 使用 `dig valuecell.hivince.com` 验证 DNS

---

**部署完成后，你就可以通过 https://valuecell.hivince.com 访问你的个人 ValueCell 实例了！** 🎉
