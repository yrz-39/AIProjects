# AI 问答卡与复习提纲助手

> 一个用于学习 AI 应用开发的本地 Python 项目。当前已完成项目环境、FastAPI 网页、SQLite 笔记持久化与课程分类；下一阶段将先用假 LLM 打通问答卡生成流程。

## 1. 项目目标

用户可以在本地网页中：

```text
填写课程、标题和笔记正文
        ↓
保存为本地笔记
        ↓
查看全部笔记或指定笔记
        ↓
后续生成复习提纲或问答卡
```

这个项目的重点不是快速拼出一个 AI Demo，而是在理解每一层作用的前提下，亲手完成一次完整的 AI 应用开发闭环：

```text
Python 工程
→ Web 请求与响应
→ SQLite 数据持久化
→ 假 LLM 流程
→ 真实模型 API
→ 结构化输出、错误处理与项目收束
```

## 2. 当前状态

| 阶段 | 状态 | 内容 |
|---|---|---|
| 阶段 A：项目与最小网页 | 已完成 | Python 3.11、uv、FastAPI、HTML 表单、GET/POST 路由 |
| 阶段 B：SQLite 笔记保存 | 已完成 | 笔记增查、按 ID 查看、404、课程分类、数据库迁移 |
| 阶段 C：假 LLM | 下一阶段 | 固定返回结构化问答卡，先打通业务流程 |
| 阶段 D：真实模型 API | 未开始 | OpenAI-compatible API、Prompt、JSON 解析与异常处理 |
| 阶段 E：测试与收束 | 未开始 | 测试补全、HTML 转义、README 完善与本地复现验证 |

> 当前项目尚未执行 Git commit 或 push。工作区中的 SQLite 数据库、缓存和虚拟环境不应提交。

## 3. 技术栈

- Python 3.11
- `uv`：虚拟环境、依赖与锁文件管理
- FastAPI：Web 应用框架
- Uvicorn：运行 FastAPI 的 ASGI 服务器
- SQLite：本地嵌入式数据库
- 原生 HTML：当前页面展示与表单
- pytest：当前已有基础测试依赖与 1 条输入校验测试

暂不使用：React、SQLAlchemy、Docker、RAG、Embedding、向量数据库、多 Agent、用户登录。

## 4. 项目目录

```text
AiStudyAssistant/
├── .gitignore
├── .python-version             # 固定项目使用 Python 3.11
├── pyproject.toml              # 项目元数据与依赖
├── uv.lock                     # 依赖版本锁定
├── README.md
├── .venv/                      # 项目专属 Python 环境，不提交
├── .vscode/
│   └── setting.json            # VS Code 解释器设置
├── .hermes/
│   └── plans/                  # 项目学习蓝图
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用、页面与路由
│   ├── note_validation.py      # 笔记正文清理
│   ├── database.py             # SQLite 连接、建表与迁移
│   └── repositories.py         # notes 表的增查操作
├── data/
│   └── app.db                 # SQLite 数据库，运行时自动生成
└── tests/
    └── test_note_validation.py
```

## 5. 环境准备

项目位于 D 盘，与 C++ 工程分开：

```text
D:\CppProject\       # C++ 与数据结构工程
D:\AiProjects\       # Python 与 AI 工程
```

创建项目虚拟环境：

```bash
uv venv --python 3.11
```

初始化项目：

```bash
uv init --bare --name ai-study-assistant --python 3.11 --vcs git --no-workspace
uv python pin 3.11
```

安装运行依赖：

```bash
uv add fastapi "uvicorn[standard]"
```

安装开发测试依赖：

```bash
uv add --dev pytest
```

## 6. 启动与停止

在项目根目录启动开发服务器：

```bash
uv run uvicorn app.main:app --reload
```

浏览器打开：

```text
http://127.0.0.1:8000
```

停止服务：

```text
Ctrl + C
```

若 8000 端口已被其他 Uvicorn 进程占用，可以临时使用：

```bash
uv run uvicorn app.main:app --reload --port 8001
```

## 7. 当前 API

| 方法 | 路径 | 作用 | 当前返回 |
|---|---|---|---|
| `GET` | `/` | 打开笔记输入首页 | HTML |
| `POST` | `/api/notes` | 创建一篇笔记 | HTML 成功页 |
| `GET` | `/api/notes` | 查看全部笔记 | HTML 列表页 |
| `GET` | `/api/notes/{note_id}` | 查看指定笔记 | HTML 详情页；不存在时 404 JSON |

### 当前 POST 表单字段

```text
course    可选，课程名称，例如“数据结构”
title     可选，笔记标题
content   必填，笔记正文
```

### 手工验证示例

```text
1. 打开 http://127.0.0.1:8000
2. 填写课程、标题和正文
3. 点击“提交笔记”
4. 打开 /api/notes 查看列表
5. 根据列表中的 ID 打开 /api/notes/{id}
6. 打开一个不存在的 ID，例如 /api/notes/999999
```

不存在的笔记应返回：

```json
{
  "detail": "笔记不存在"
}
```

HTTP 状态码应为：

```text
404 Not Found
```

## 8. 已实现的关键逻辑

### 8.1 输入清理

`app/note_validation.py` 负责清理正文首尾空白，并处理空字符串或全空白字符串：

```text
"  链表是一种线性结构。  "
        ↓
"链表是一种线性结构。"
```

当前实现使用双指针从两端扫描，再使用字符串切片取出有效区间。重点学习了：

- 字符串索引；
- `\t`、`\n` 转义字符；
- Python 切片左闭右开；
- 空字符串和全空白边界；
- 函数输入与返回值类型注解。

### 8.2 数据库初始化与迁移

数据库文件由 SQLite 自动生成：

```text
data/app.db
```

初始化流程：

```text
get_connection()
→ CREATE TABLE IF NOT EXISTS notes
→ PRAGMA table_info(notes) 检查列结构
→ 如果缺少 course，执行 ALTER TABLE
→ commit()
→ close()
```

之所以不能用 `list_notes()` 检查列，是因为 `list_notes()` 查询的是业务数据，而不是数据库结构；数据库初始化应使用 SQLite 的元数据查询 `PRAGMA table_info(notes)`。

### 8.3 Repository 层

`repositories.py` 将数据库读写从 FastAPI 路由中分离出来：

```text
main.py
→ 负责 HTTP 与页面

repositories.py
→ 负责 INSERT / SELECT

database.py
→ 负责连接与表结构
```

数据库查询使用参数化 SQL：

```python
conn.execute(
    "INSERT INTO notes (course, title, content) VALUES (?, ?, ?)",
    (course, title, content),
)
```

不能把用户输入直接拼接进 SQL 字符串，以避免 SQL 注入。

### 8.4 FastAPI 路径参数与 404

```python
@app.get("/api/notes/{note_id}")
def view_note(note_id: int):
    note = repo.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
```

这里的 `{note_id}` 是路径参数。FastAPI 会把 URL 中的文本转换成 `int`，再传给函数。

## 9. 时间线与实现步骤

### 2026-07-23 至 2026-07-24：环境与项目骨架

- 确定项目方向：AI 问答卡 / 复习提纲助手。
- 决定所有项目代码放在 D 盘：`D:\AiProjects\AiStudyAssistant`。
- 使用 Python 3.11 建立独立 `.venv`。
- 用 `uv init --bare` 建立 Python 项目。
- 用 `.python-version` 固定 Python 3.11。
- 安装 FastAPI、Uvicorn、pytest。
- 解决 VS Code Pylance 解释器指向错误的问题。
- 认识 `pyproject.toml`、`uv.lock`、项目虚拟环境和 Python 模块导入。

### 2026-07-24：第一段 Python 与最小 Web

- 编写 `validate_note()`。
- 通过交互式 Python 手动验证正常文本、首尾空白、全空白和转义字符。
- 建立 `app/` 与 `tests/` 包结构。
- 创建最小 FastAPI 应用。
- 用 HTML 表单接收课程笔记。
- 理解 GET、POST、路由、表单字段、`Form()` 与 `HTMLResponse`。
- 处理端口占用、错误解释器和模块搜索路径问题。

### 2026-08-03：SQLite 与阶段 B 收束

- 使用标准库 `sqlite3` 创建本地数据库。
- 建立 `notes` 表，理解表、行、列、主键和时间戳。
- 实现 `add_note()` 与 `list_notes()`。
- 使用参数化 SQL 保存数据。
- 实现 `get_note(note_id)` 与单条详情路由。
- 对不存在的笔记返回 HTTP 404。
- 使用 `PRAGMA table_info(notes)` 检查真实表结构。
- 通过 `ALTER TABLE` 将旧数据库迁移，新增 `course` 列。
- 修改网页表单、POST 路由、列表页和详情页，完整接入课程分类。
- 实际验证保存、列表、详情、404，并确认 pytest 现有测试通过。

## 10. 下一阶段

阶段 C 先不调用真实模型，而是建立假 LLM：

```text
选择一篇笔记
→ 调用本地假 client
→ 返回固定 JSON 问答卡
→ 保存 generation 记录
→ 页面展示结果
```

计划新增的概念：

- `generations` 表；
- `note_id` 外键关系；
- `outline` / `flashcards` 模式；
- Python 字典与 JSON 的序列化、反序列化；
- 可替换的 LLM client；
- 为什么先用假服务打通流程，再接真实 API。

## 11. 当前待改进项

这些不是当前阶段的阻塞问题，但在项目收束前需要处理：

- 使用 HTML 转义，避免用户输入直接插入 HTML；
- 将内嵌 HTML 页面拆分为模板或静态文件；
- 使用 Pydantic schema 统一 API 输入输出；
- 为数据库操作、空内容、404 和生成流程补充测试；
- 完善异常处理和连接释放策略；
- 增加列表页到详情页的链接；
- 接入真实模型前补 `.env.example`，绝不提交真实 API Key。

## 12. 相关学习笔记

- [[AI辅助项目/AI知识点总结助手项目/项目搭建记录-阶段A与阶段B]]
- 项目学习蓝图：`.hermes/plans/2026-07-23_ai-flashcard-assistant-learning-blueprint.md`
