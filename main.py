import os
import openai

# 确保设置环境变量: export OPENAI_API_KEY="your-key"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://openai.com")

class CodeReviewAgentSystem:
    def __init__(self, model="gpt-4o"):
        self.model = model

    def _call_llm(self, system_prompt, user_content):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.2
            )
            return response.choices.message['content']
        except Exception as e:
            return f"API 调用失败: {str(e)}"

    def agent_security_scanner(self, code):
        """Agent A: 漏洞扫描员"""
        prompt = "你是一个顶级的安全专家和代码审计师。请检查以下代码中的潜在 Bug、性能瓶颈或安全漏洞。请条理清晰地列出问题。"
        return self._call_llm(prompt, f"请审计以下代码：\n\n{code}")

    def agent_architect_refactor(self, code, review_report):
        """Agent B: 架构重构师"""
        prompt = "你是一个精通设计模式的资深架构师。请结合代码本身和评审报告，对代码进行重构优化。只输出优化后的完整代码，不要包含多余的解释。"
        user_content = f"原始代码：\n{code}\n\n评审报告：\n{review_report}"
        return self._call_llm(prompt, user_content)

    def agent_test_validator(self, original_code, refactored_code):
        """Agent C: 测试验证员"""
        prompt = "你是一个专业的 QA 自动化测试专家。请针对原始代码的功能，为重构后的代码编写一份单元测试脚本（使用 pytest 框架），以验证功能的一致性。"
        user_content = f"原始代码：\n{original_code}\n\n重构后的代码：\n{refactored_code}"
        return self._call_llm(prompt, user_content)

    def run_workflow(self, target_code):
        print(" [1/3] Agent A 正在进行安全与性能审计...")
        review_report = self.agent_security_scanner(target_code)
        print("\n--- 评审报告 ---\n", review_report)
        
        print("\n [2/3] Agent B 正在根据报告进行代码重构...")
        refactored_code = self.agent_architect_refactor(target_code, review_report)
        print("\n--- 重构后的代码 ---\n", refactored_code)
        
        print("\n [3/3] Agent C 正在生成单元测试以进行闭环验证...")
        test_cases = self.agent_test_validator(target_code, refactored_code)
        print("\n--- 自动生成的单元测试 ---\n", test_cases)
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
