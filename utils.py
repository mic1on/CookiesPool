def import_object(name: str):
    """字符串导入模块方法"""
    if name.count(".") == 0:
        return __import__(name)
    parts = name.split(".")
    obj = __import__(".".join(parts[:-1]), fromlist=[parts[-1]])
    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError("No module named %s" % parts[-1])