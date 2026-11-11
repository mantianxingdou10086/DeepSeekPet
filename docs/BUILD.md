# 源码运行、构建与测试

## 环境与输入

支持目标是 Windows 10/11 x64。1.0.0 本地构建使用 Python 3.11、Pillow 12.3.0、pystray 0.19.5、PyInstaller 6.22.3。Python 必须带 Tcl/Tk；`pet.py` 使用 Windows Arial 字体路径和 Tk 透明色属性。

运行：`python -m pip install -r requirements.txt` 后执行 `python pet.py`。建议使用 README 中的独立虚拟环境。正式版和源码版共享单实例锁及用户设置，不应同时作为日常实例运行。

## 构建便携目录

```powershell
python -m pip install -r requirements-build.txt
python -m PyInstaller --noconfirm DeepSeekPet.spec
```

必须从仓库根目录执行。spec 所需的 `pet.py`、四个运行模块、`pet.ico`、`version_info.txt` 和六组素材均在仓库中，无需额外私有文件、下载模型或重新生成素材。

`dist/DeepSeekPet/DeepSeekPet.exe` 与 `_internal` 必须一起交付。可将整个 `DeepSeekPet` 目录与面向用户的 README 一起压成 ZIP；不能只压 EXE。构建输出不进入 Git。该命令不会自动生成与已发布 ZIP 字节一致的归档；第三方依赖、时间戳和构建环境可能影响产物。

## 测试

```powershell
python pet.py --test
python run_acceptance.py
```

`--test` 打开短暂真实 Tk 窗口，检查透明、置顶、缩放、气泡与暂停后退出。

验收入口显式列出 16 项脚本，覆盖动作节奏、起床帧、喂食、专注、睡眠、工作区、隐藏提醒、暂停和桌面运行集成。运行会生成本地 `acceptance-results.txt`（忽略，不入库）。

**测试前请退出日常桌宠**：部分测试会创建托盘、暂时读写并恢复用户设置，单实例测试也需要取得锁。不要在正在使用的正式进程旁直接运行整套验收。发布上传本身不需要重建，也不会停止现有程序。

历史实验 `test_focus_pause.py` 要求“暂停专注计时”，与当前产品语义相反，因此没有包含在仓库或验收中；不能把它计为通过。模拟双屏/移屏测试不等同于物理拔屏实验。

## 发布边界

当前 v1.0.0 使用既有正式 ZIP，不因文档更新而重建。发布前记录中 16 项验收通过，完整 ZIP 做过 CRC 检查、实际解压与独立 Tk 冒烟；这些是特定环境验证，不是任意机器兼容性或长期无泄漏保证。程序没有代码签名。
