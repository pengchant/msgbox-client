from datetime import datetime


class MyDateInfoHelper:
    """日期时间格式化工具类"""

    @staticmethod
    def getTimeRange():
        hour = datetime.now().hour
        if 0 <= hour < 4:
            return "深夜"
        elif hour < 9:
            return "早上"
        elif hour < 12:
            return "上午"
        elif hour < 14:
            return "中午"
        elif hour < 18:
            return "下午"
        else:
            return "晚上"
