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

**对于开发者**，需要安装 pre-commit 脚本，用于检查代码规范:

```bash
pre-commit install
```

## 数据集构建流程

数据集构建流程如下：
* `data_extract`: 从原始数据中提取每章节的文本数据，将每章节转化为一个文件。
* `data_process`: 将上述生成的章节文件，根据原始语言与目标语言，进行句子对齐。
* `data_report`: 将句子对齐的结果进行可视化，目前支持 HTML。

### 文本数据抽取

详见 `data_extract` 中，目前支持将 epub 中的章节抽取。

### 章节句子对齐

详见 `data_process` 中，将同一章节的不同语种对应后，可以生成各章节中的句子对应结果。

### 对齐可视化

详见 `data_report` 中，可以对 JSON 形式的对齐结果进行可视化。
