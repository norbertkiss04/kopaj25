from fastapi import APIRouter, Request
from typing import List, Optional
from collections import deque
import json

router = APIRouter(prefix="/level1/task2")

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr: List[int]) -> Optional[TreeNode]:
    if not arr or arr[0] == -1:
        return None
    
    root = TreeNode(arr[0])
    queue = deque([root])
    i = 1
    n = len(arr)
    
    while i < n:
        curr = queue.popleft()
        
        # Left child
        if i < n:
            val = arr[i]
            i += 1
            if val != -1:
                curr.left = TreeNode(val)
                queue.append(curr.left)
        
        # Right child
        if i < n:
            val = arr[i]
            i += 1
            if val != -1:
                curr.right = TreeNode(val)
                queue.append(curr.right)
                
    return root

def zigzag_level_order(root: Optional[TreeNode]) -> List[int]:
    if not root:
        return []
    
    result = []
    queue = deque([root])
    left_to_right = True
    
    while queue:
        level_size = len(queue)
        level_nodes = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level_nodes.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        if not left_to_right:
            level_nodes.reverse()
            
        result.extend(level_nodes)
        left_to_right = not left_to_right
        
    return result

@router.post("")
async def zigzag_tree(request: Request):
    body = await request.body()
    arr = json.loads(body.decode('utf-8'))
    root = build_tree(arr)
    return zigzag_level_order(root)