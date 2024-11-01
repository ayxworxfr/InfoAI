import logging
import os


def get_path_from_root(path):
    real_path = ""
    # 判断是否是相对路径
    if not os.path.isabs(path):
        # 获取项目根目录
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        real_path = os.path.join(root_path, path)
    else:
        real_path = path
    return real_path


def get_logger():
    # 配置日志格式和日志输出目录
    log_path = get_path_from_root("logs/dag.log")

    # 判断是否manual
    if os.getenv("MANUAL", "false") == "true":
        log_path = get_path_from_root("logs/test_dag.log")

    # 确保路径存在
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    handler = logging.FileHandler(log_path, mode="a")  # 添加文件输出
    format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(format)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(format)
    handlers = [handler, console_handler]

    log = logging.getLogger("dag")
    log.setLevel(logging.INFO)
    log.handlers = handlers
    return log


log = get_logger()

__all__ = ["log"]
