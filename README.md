# DeepSeekPet · DeepSeek 桌宠

一只离线陪伴你学习和工作的 Windows 桌宠：摸摸头、喂 Token、吃白饭，或让她在你专注时敲键盘。

> **非官方同人项目**：与 DeepSeek 公司没有隶属、合作或官方授权关系，不是 DeepSeek 官方产品。没有接入大模型，不提供 AI 聊天，也不需要 API Key。

<p align="center"><img src="assets/layered/00.png" width="240" alt="DeepSeekPet 角色待机素材"></p>

## 下载即用

前往 [v1.0.0 Releases](https://github.com/mantianxingdou10086/DeepSeekPet/releases/tag/v1.0.0)，下载 **DeepSeekPet-1.0.0-windows-x64.zip**，完整解压后双击 `DeepSeekPet/DeepSeekPet.exe`。

- 面向 Windows 10/11 x64；无需安装 Python 或 Hermes。
- **请保留 EXE 旁的整个 `_internal` 目录**，不能只复制 EXE。更新前退出旧版，再替换整个程序目录。
- 本程序未进行商业代码签名，Windows 可能提示未知发布者；请核对下载来源及 Release 中的 SHA256。
- 未宣称已在干净虚拟机或所有多屏/DPI 组合上完成实测。

## 可以做什么

| 操作 | 效果 |
| --- | --- |
| 左键拖动 / 单击 | 移动桌宠 / 摸头，睡着时叫醒 |
| 右键菜单 | 专注陪伴、打盹、喂食、暂停、尺寸和退出 |
| 专注陪伴 | 5 / 25 / 45 分钟倒计时，结束提醒 |
| 喂 Token / 吃白饭 | 两种不同的喂食动画；Token 是视觉道具，不会产生 API 费用 |
| 自动打盹 | 空闲五分钟后休息，可在菜单关闭 |
| 暂停动画 | 冻结角色及当前动作；**专注计时不暂停** |
| 隐藏到托盘 | 隐藏角色和小窗；完成提醒在恢复时只补一次 |
| 托盘显示 / 退出 | 找回桌宠或完全关闭；重复启动不会生成第二只 |

窗口位置会限制到显示器工作区，支持负坐标副屏；显示器变化后周期检查位置。位置、尺寸和自动打盹偏好保存在 `%LOCALAPPDATA%\DeepSeekPet\settings.json`，滚动日志在同目录。退出后不会保存专注进度。详见 [使用说明](docs/USAGE.md)。

## 从源码运行

需要 **Windows、Python 3.11 x64（含 Tcl/Tk）**。在项目目录执行：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe pet.py
```

如果正式版已在运行，单实例保护会让新启动立即退出；请先从托盘退出已有桌宠。源码用到 Windows 的透明色窗口、工作区 API 和系统字体，不以 macOS/Linux 为支持平台。

## 开发与构建

技术栈：Python 3.11、Tkinter、Pillow、pystray；PyInstaller 生成便携目录。依赖版本取自 1.0.0 本地构建环境。

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm DeepSeekPet.spec
```

输出为 `dist/DeepSeekPet/`，需整体分发。必要动画、图标和版本文件均已入库，无需重新生成 AI 图片。详见 [构建与测试](docs/BUILD.md)。

```text
pet.py                    角色窗口、状态和交互
motion_timing.py          动作帧节奏
window_bounds.py          显示器工作区与坐标夹紧
desktop_runtime.py        托盘、单实例、设置与滚动日志
assets/                   175 张运行必需动画 PNG
pet.ico                   程序/托盘图标
DeepSeekPet.spec           PyInstaller 构建入口
run_acceptance.py         明确列出的 16 项回归脚本入口
docs/                     使用、构建、素材说明
```

仓库不包含桌面截图、聊天界面截图、个人设置、日志、备份、生成过程的临时文件或打包运行库；便携 ZIP 仅作为 Release 附件发布。

## 素材来源、版权与授权边界

角色相关图片使用 AI 辅助生成（本地制作过程使用 Gemini），再经过透明背景处理、分层、帧整理和动画节奏编辑。这里的 175 张 PNG 是应用运行素材，不是聊天截图或素材生成记录。详见 [素材说明](docs/ASSETS.md)。

DeepSeek 名称及相关品牌权益属于其各自权利人。项目未宣称拥有官方角色授权，也不承诺 AI 生成内容具有排他性或适用于任何商业用途。

**本仓库尚未指定开源许可证。公开可见不等于授予任意复制、再分发或商业使用的许可。** 第三方依赖及其随包组件分别遵循各自许可证；对源码或素材的再利用，请先确认相应授权。
