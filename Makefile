# 定义Python解释器
PYTHON := python3

# 定义pip包安装程序
PIP := pip3

# 定义项目目录
PROJECT_DIR := .

# 定义Python模块搜索路径
PYTHONPATH := $(PROJECT_DIR):$(PROJECT_DIR)/dags

# 定义虚拟环境目录
VENV_DIR := venv

# 定义依赖文件
REQUIREMENTS := requirements.txt

# 定义测试运行器
TEST_RUNNER := pytest

# 定义代码风格检查器
STYLE_CHECKER := flake8

# 定义类型检查器
TYPE_CHECKER := mypy

# 定义Sphinx文档构建器
DOC_BUILDER := sphinx-build

# 定义构建物目录
BUILD_DIR := build

.PHONY: all install clean test style type-check docs

# 默认目标
all: install

# 安装依赖并设置虚拟环境
install:
	@echo "设置虚拟环境..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "安装依赖..."
	$(VENV_DIR)/bin/$(PIP) install -r $(REQUIREMENTS)

# 使用pytest运行测试
test:
	@echo "运行测试..."
	PYTHONPATH=$(PYTHONPATH) $(VENV_DIR)/bin/$(TEST_RUNNER) $(PROJECT_DIR)/tests

# 使用flake8检查代码风格
style:
	@echo "检查代码风格..."
	$(VENV_DIR)/bin/$(STYLE_CHECKER) $(PROJECT_DIR)

# 使用mypy进行类型检查
type-check:
	@echo "进行类型检查..."
	$(VENV_DIR)/bin/$(TYPE_CHECKER) $(PROJECT_DIR)

# 使用Sphinx构建文档
docs:
	@echo "构建文档..."
	$(DOC_BUILDER) -b html docs/source $(BUILD_DIR)/html

# 清理构建和Python生成的文件
clean:
	@echo "清理构建和Python生成的文件..."
	rm -rf $(BUILD_DIR)
	rm -rf $(VENV_DIR)
	find $(PROJECT_DIR) -type f -name '*.py[co]' -delete
	find $(PROJECT_DIR) -type d -name '__pycache__' -delete

# make run file=${file} 运行指定的Python文件
run:
	@echo "运行Python文件, file: $(file)"
	PYTHONPATH=$(PYTHONPATH) $(VENV_DIR)/bin/$(PYTHON) $(file)
