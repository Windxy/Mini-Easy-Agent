from collections import deque
from typing import Iterable, Optional, TypeVar

_T = TypeVar('_T')

# 固定首位的队列
class FixedFrontDeque(deque):
    def __init__(self, iterable: Optional[Iterable[_T]], maxlen: Optional[int] = None) -> None:
        super().__init__(iterable, maxlen)
        # 固定首位，在初始化时将首位固定
        self.fixed_front = iterable[0]

    # 每次插入，将首位固定
    def append(self, x: _T) -> None:
        super().append(x)
        self[0] = self.fixed_front
    
    # 清除队列，保留首位
    def clear(self) -> None:
        super().clear()
        self.append(self.fixed_front)
    
if __name__ == '__main__':
    # 使用示例
    q = FixedFrontDeque(iterable=[0],maxlen=4)
    q.append(1)
    print(q)  # 输出: 0,1
    q.append(2)
    print(q)  # 输出: 0,1,2
    q.append(3)
    print(q)  # 输出: 0,1,2,3
    q.append(4)
    print(q)  # 输出: 0,2,3,4
    q.clear()   
    print(q)  # 输出: 0