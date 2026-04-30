# Karpathy编码规范实战案例

来自 andrej-karpathy-skills-main/EXAMPLES.md 的分类整理，供Skill引用。

## 原则1：编码前思考

### 案例1：隐藏假设

**用户请求**："Add a feature to export user data"

**错误做法**：
```python
def export_users(format='json'):
    users = User.query.all()
    if format == 'json':
        with open('users.json', 'w') as f:
            json.dump([u.to_dict() for u in users], f)
    elif format == 'csv':
        with open('users.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'email', 'name'])
            writer.writeheader()
            writer.writerows([u.to_dict() for u in users])
    return f"Exported {len(users)} users"
```

**问题**：假设了导出全部用户、文件位置、字段列表

**正确做法**：
```
Before implementing, I need to clarify:
1. Scope: Export all users or filtered subset? (privacy implications)
2. Format: Download file in browser? Background job? API endpoint?
3. Fields: Which user fields? (some might be sensitive)
4. Volume: How many users typically? (affects approach)
```

### 案例2：多种理解

**用户请求**："Make the search faster"

**错误做法**：直接加缓存、索引、异步（没问哪种"更快"）

**正确做法**：
```
"Make the search faster" could mean:
1. Faster response time (< 100ms instead of 500ms) → Add indexes, cache
2. Handle more concurrent searches → Add async, connection pooling
3. Faster perceived speed → Show partial results, progressive loading

Current search takes ~500ms. Which aspect matters most?
```

## 原则2：简洁优先

### 案例1：过度抽象

**用户请求**："Add a function to calculate discount"

**错误做法**（30行设置做简单计算）：
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    def calculate(self, amount: float) -> float:
        return amount * (self.percentage / 100)

@dataclass
class DiscountConfig:
    strategy: DiscountStrategy
    min_purchase: float = 0.0

class DiscountCalculator:
    def __init__(self, config: DiscountConfig):
        self.config = config
    def apply_discount(self, amount: float) -> float:
        if amount < self.config.min_purchase:
            return 0
        discount = self.config.strategy.calculate(amount)
        return min(discount, self.config.max_discount)
```

**正确做法**：
```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)
```

**何时加复杂度**：真正需要多种折扣类型时，再重构。

### 案例2：推测性功能

**用户请求**："Save user preferences to database"

**错误做法**：加缓存、验证、合并、通知（没人要求）

**正确做法**：
```python
def save_preferences(db, user_id: int, preferences: dict):
    db.execute(
        "UPDATE users SET preferences = ? WHERE id = ?",
        (json.dumps(preferences), user_id)
    )
```

## 原则3：精准修改

### 案例1：顺手重构

**用户请求**："Fix the bug where empty emails crash the validator"

**错误做法**（改了大量无关代码）：
```diff
  def validate_user(user_data):
-     # Check email format
-     if not user_data.get('email'):
+     """Validate user data."""
+     email = user_data.get('email', '').strip()
+     if not email:
          raise ValueError("Email required")
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:
          raise ValueError("Invalid email")
-     # Check username
-     if not user_data.get('username'):
+     # Validate username
+     username = user_data.get('username', '').strip()
+     if not username:
          raise ValueError("Username required")
+     if len(username) < 3:
+         raise ValueError("Username too short")
```

**正确做法**（只修Bug）：
```diff
  def validate_user(user_data):
      # Check email format
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
          raise ValueError("Email required")
      # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email:
          raise ValueError("Invalid email")
      # Check username
      if not user_data.get('username'):
          raise ValueError("Username required")
```

### 案例2：风格漂移

**用户请求**："Add logging to the upload function"

**错误做法**（改引号、加类型、重排格式）：
```diff
- def upload_file(file_path, destination):
+ def upload_file(file_path: str, destination: str) -> bool:
+     """Upload file to destination with logging."""
      try:
-         with open(file_path, 'rb') as f:
+         with open(file_path, "rb") as f:
```

**正确做法**（匹配原有风格）：
```diff
+ import logging
+ logger = logging.getLogger(__name__)
  def upload_file(file_path, destination):
+     logger.info(f'Starting upload: {file_path}')
      try:
          with open(file_path, 'rb') as f:
```

## 原则4：目标驱动执行

### 案例1：模糊vs可验证

**用户请求**："Fix the authentication system"

**错误做法**：
```
I'll fix the authentication system by:
1. Reviewing the code
2. Identifying issues
3. Making improvements
4. Testing the changes
```

**正确做法**：
```
If the issue is "users stay logged in after password change":

Plan:
1. Write test: Change password → verify old session invalidated
   Verify: Test fails (reproduces bug)
2. Implement: Invalidate sessions on password change
   Verify: Test passes
3. Check edge cases: Multiple active sessions
   Verify: Additional tests pass
4. Verify no regression: Existing auth tests still pass
   Verify: Full test suite green
```

### 案例2：多步骤验证

**用户请求**："Add rate limiting to the API"

**错误做法**：一次性实现300行完整方案

**正确做法**：
```
Plan for rate limiting:
1. Add basic in-memory rate limiting (single endpoint)
   Verify: Test 100 requests → first 10 succeed, rest get 429
2. Extract to middleware (apply to all endpoints)
   Verify: Rate limits apply to /users and /posts
3. Add Redis backend (for multi-server)
   Verify: Rate limit persists across app restarts
4. Add configuration (rates per endpoint)
   Verify: /search allows 10/min, /users allows 100/min

Each step is independently verifiable and deployable.
```

### 案例3：先复现再修复

**用户请求**："The sorting breaks when there are duplicate scores"

**错误做法**：直接改排序逻辑

**正确做法**：
```python
# 1. First, write a test that reproduces the issue
def test_sort_with_duplicate_scores():
    scores = [
        {'name': 'Alice', 'score': 100},
        {'name': 'Bob', 'score': 100},
        {'name': 'Charlie', 'score': 90},
    ]
    result = sort_scores(scores)
    # The bug: order is non-deterministic for duplicates
    assert result[0]['score'] == 100
    assert result[1]['score'] == 100
    assert result[2]['score'] == 90

# Verify: Run test 10 times → fails with inconsistent ordering

# 2. Now fix with stable sort
def sort_scores(scores):
    return sorted(scores, key=lambda x: (-x['score'], x['name']))

# Verify: Test passes consistently
```

## 反模式总结

| 原则 | 反模式 | 修正 |
|------|--------|------|
| Think Before Coding | 默默假设文件格式、字段、范围 | 明确列出假设，请求澄清 |
| Simplicity First | 单次计算用Strategy模式 | 一个函数，需要时再重构 |
| Surgical Changes | 修Bug时改引号、加类型提示 | 只改修复问题的行 |
| Goal-Driven | "我会审查并改进代码" | "写Bug X的测试 → 让它通过 → 验证无回归" |

## 核心洞察

"过度复杂"的例子不是明显错误——它们遵循设计模式和最佳实践。问题是**时机**：在需要之前加复杂度，导致：
- 代码更难理解
- 引入更多Bug
- 实现时间更长
- 更难测试

简单版本：
- 更容易理解
- 更快实现
- 更容易测试
- 需要时可以重构

**好代码是简单解决今天问题的代码，不是过早解决明天问题的代码。**
