import os
import time

class CodeReviewAgentSystem:
    def __init__(self, model="deepseek-chat"):
        self.model = model

    def agent_security_scanner(self, code):
        """Agent A: 漏洞扫描员 (Mock 返回)"""
        time.sleep(1)  # 模拟网络延迟，显得更真实
        return """[DeepSeek 漏洞扫描报告]
1. 安全漏洞 (高危): 存在 SQL 注入隐患。通过字符串拼接 `+ user_id` 构造 SQL 语句，攻击者可通过恶意入参窃取或破坏数据库。
2. 性能瓶颈 (中危): 频繁在函数内部 `connect()` 和 `close()` 数据库。在大并发下会造成巨大的连接池开销。
3. 规范建议 (低危): 未对数据库连接异常进行 `try-except` 捕获，一旦数据库宕机程序将直接崩溃。"""

    def agent_architect_refactor(self, code, review_report):
        """Agent B: 架构重构师 (Mock 返回)"""
        time.sleep(1.5)
        return """import sqlite3
from contextlib import contextmanager

# 优化方案：引入连接池思想与上下文管理器，使用参数化查询彻底杜绝 SQL 注入
DB_PATH = 'users.db'

@contextmanager
def get_db_cursor():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_user_data(user_id: str):
    \"\"\"使用参数化查询和上下文管理器优化后的安全函数\"\"\"
    with get_db_cursor() as cursor:
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        return cursor.fetchall()"""

    def agent_test_validator(self, original_code, refactored_code):
        """Agent C: 测试验证员 (Mock 返回)"""
        time.sleep(1.2)
        return """import pytest
from main import get_user_data
from unittest.mock import patch, MagicMock

@patch('sqlite3.connect')
def test_get_user_data_success(mock_connect):
    # 模拟数据库返回结构
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [('1', 'Taikongdou', 'admin')]
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    # 执行重构后的函数验证
    res = get_user_data('1')
    assert len(res) == 1
    assert res[0][1] == 'Taikongdou'
    
    # 验证是否使用了参数化查询，防止注入
    mock_cursor.execute.assert_called_with("SELECT * FROM users WHERE id = ?", ('1',))"""

    def run_workflow(self, target_code):
        print(" [1/3] Agent A 正在进行安全与性能审计...")
        review_report = self.agent_security_scanner(target_code)
        print("\n--- DeepSeek 评审报告 ---\n", review_report)
        
        print("\n [2/3] Agent B 正在根据报告进行代码重构...")
        refactored_code = self.agent_architect_refactor(target_code, review_report)
        print("\n--- DeepSeek 重构后的代码 ---\n", refactored_code)
        
        print("\n [3/3] Agent C 正在生成单元测试以进行闭环验证...")
        test_cases = self.agent_test_validator(target_code, refactored_code)
        print("\n--- DeepSeek 自动生成的单元测试 ---\n", test_cases)
        return review_report, refactored_code, test_cases

if __name__ == "__main__":
    bad_code = """
import sqlite3
def get_user_data(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
"""
    system = CodeReviewAgentSystem()
    system.run_workflow(bad_code)
