# acg_corpus_ja_zh

日文到中文的 ACG(主要是轻小说) 文本数据集。

## 克隆仓库

仓库里使用了 [vecalign](https://github.com/thompsonb/vecalign) 子仓库。

如果未克隆仓库，使用以下命令克隆：

```bash
git clone --recurse-submodules git@github.com:leonardodalinky/acg_corpus_ja_zh.git
```

如果已经 clone 了前面版本，则需要同步子模块：

```bash
git submodule update --recursive
```

## 依赖设置

要有 PyTorch 环境，因为使用了 Hugging Face 的 sentence-transformers。

```
pip install -r requirements.txt
```
