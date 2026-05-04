from collections import deque
import sys

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.profile = None 

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, user_id, profile):
        self.root = self._insert(self.root, user_id, profile)
    
    def _insert(self, node, user_id, profile):
        if not node:
            node = TreeNode(user_id)
            node.profile = profile
            return node
        if user_id < node.key:
            node.left = self._insert(node.left, user_id, profile)
        elif user_id > node.key:
            node.right = self._insert(node.right, user_id, profile)
        else:
            node.profile = profile  
        return node
    
    def search(self, user_id):
        node = self._search(self.root, user_id)
        return node.profile if node else None
    
    def _search(self, node, user_id):
        if not node or node.key == user_id:
            return node
        if user_id < node.key:
            return self._search(node.left, user_id)
        return self._search(node.right, user_id)
    
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.profile))
            self._inorder(node.right, result)

class HashTable:
    def __init__(self, size=11):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, user_id):
        return hash(user_id) % self.size
    
    def insert(self, user_id, profile):
        index = self._hash(user_id)
        bucket = self.table[index]
        for i, (uid, prof) in enumerate(bucket):
            if uid == user_id:
                bucket[i] = (user_id, profile)
                return
        bucket.append((user_id, profile))
    
    def get(self, user_id):
        index = self._hash(user_id)
        for uid, profile in self.table[index]:
            if uid == user_id:
                return profile
        return None
    
    def delete(self, user_id):
        index = self._hash(user_id)
        bucket = self.table[index]
        for i, (uid, _) in enumerate(bucket):
            if uid == user_id:
                bucket.pop(i)
                return True
        return False

class SocialGraph:
    def __init__(self):
        self.graph = {}
    
    def add_user(self, user_id):
        if user_id not in self.graph:
            self.graph[user_id] = []
    
    def add_friendship(self, user1, user2):
        self.add_user(user1)
        self.add_user(user2)
        if user2 not in self.graph[user1]:
            self.graph[user1].append(user2)
        if user1 not in self.graph[user2]:
            self.graph[user2].append(user1)
    
    def remove_friendship(self, user1, user2):
        if user1 in self.graph:
            self.graph[user1] = [f for f in self.graph[user1] if f != user2]
        if user2 in self.graph:
            self.graph[user2] = [f for f in self.graph[user2] if f != user1]
    
    def get_friends(self, user_id):
        return self.graph.get(user_id, [])
    
    def bfs_shortest_path(self, start, target):
        if start not in self.graph or target not in self.graph:
            return None
        
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            current, path = queue.popleft()
            if current == target:
                return path
            
            for friend in self.graph[current]:
                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, path + [friend]))
        return None
    
    def dfs_exploration(self, start, depth):
        visited = set()
        result = []
        
        def dfs(node, current_depth):
            if current_depth > depth or node in visited:
                return
            visited.add(node)
            result.append(node)
            
            for friend in self.graph.get(node, []):
                dfs(friend, current_depth + 1)
        
        dfs(start, 0)
        return result

def recommend_by_interests(profiles, target_user):
    target_interests = profiles[target_user]["interests"]
    
    recommendations = []
    for user_id, profile in profiles.items():
        if user_id == target_user:
            continue
        common = len(set(target_interests) & set(profile["interests"]))
        recommendations.append((user_id, common))
    
    return sorted(recommendations, key=lambda x: x[1], reverse=True)

class SocialNetworkExplorer:
    def __init__(self):
        self.bst = BST()  
        self.hashtable = HashTable()  
        self.graph = SocialGraph()  
        self.profiles = {}  
    
    def add_user(self, user_id, name, age, interests):
        profile = {"name": name, "age": age, "interests": interests}
        self.profiles[user_id] = profile
        self.bst.insert(user_id, profile)
        self.hashtable.insert(user_id, profile)
        self.graph.add_user(user_id)
        print(f"Added user {user_id}: {name}")
    
    def update_profile(self, user_id, **kwargs):
        if user_id in self.profiles:
            self.profiles[user_id].update(kwargs)
            self.bst.insert(user_id, self.profiles[user_id])
            self.hashtable.insert(user_id, self.profiles[user_id])
            print(f"Updated profile {user_id}")
    
    def show_profile(self, user_id):
        profile = self.hashtable.get(user_id)
        if profile:
            print(f"{user_id}: {profile['name']}, {profile['age']}yo")
            print(f"   Interests: {', '.join(profile['interests'])}")
            print(f"   Friends: {len(self.graph.get_friends(user_id))}")
        else:
            print(f"User {user_id} not found")
    
    def demo_all(self):
        print("\n" + "="*60)
        print("SOCIAL NETWORK EXPLORER - FULL DEMO")
        print("="*60)
        
        print("\n ADDING USERS...")
        users = [
            (1, "Alice", 25, ["music", "coding"]),
            (2, "Bob", 30, ["coding", "gaming"]),
            (3, "Charlie", 22, ["music", "movies"]),
            (4, "Diana", 28, ["gaming", "sports"]),
            (5, "Eve", 26, ["coding", "music"]),
            (6, "Frank", 32, ["sports", "movies"]),
            (7, "Grace", 24, ["movies", "coding"]),
            (8, "Henry", 29, ["sports", "gaming"])
        ]
        for user_id, name, age, interests in users:
            self.add_user(user_id, name, age, interests)

        print("\n UPDATING PROFILES...")
        self.update_profile(1, interests=["music", "coding", "reading"])
        self.update_profile(3, age=23)
    
        print("\n SHOWING PROFILES...")
        for uid in [1, 3, 5]:
            self.show_profile(uid)
        
        print("\n ADDING FRIENDSHIPS...")
        friendships = [
            (1,2), (1,3), (1,5), (2,4), (2,5), (3,5),
            (4,6), (4,8), (5,7), (6,7), (7,8), (3,4)
        ]
        for u1, u2 in friendships:
            self.graph.add_friendship(u1, u2)
        
        print("\n REMOVING FRIENDSHIP (1-3)...")
        self.graph.remove_friendship(1, 3)
 
        print("\n BFS SHORTEST PATHS...")
        path1 = self.graph.bfs_shortest_path(1, 7)
        path2 = self.graph.bfs_shortest_path(2, 6)
        print(f"1→7: {' → '.join(map(str, path1)) if path1 else 'No path'}")
        print(f"2→6: {' → '.join(map(str, path2)) if path2 else 'No path'}")
        
        print("\n DFS EXPLORATION...")
        print("From Alice(1), depth=2:", self.graph.dfs_exploration(1, 2))
        print("From Alice(1), depth=3:", self.graph.dfs_exploration(1, 3))
        
        print("\n RECOMMENDATIONS for Alice(1)...")
        recs = recommend_by_interests(self.profiles, 1)
        for user_id, score in recs[:5]:
            print(f"  {self.profiles[user_id]['name']} ({user_id}): {score} common interests")

def main():
    sne = SocialNetworkExplorer()
    sne.demo_all()
    
    print("\n" + "="*60)
    print("ALL CHECKLIST ITEMS DEMONSTRATED!")
    print("COMPLEXITIES:")
    print("• BST insert/search: O(log n) avg, O(n) worst")
    print("• HashTable: O(1+α) avg (separate chaining)")
    print("• BFS/DFS: O(V+E)")
    print("• Recommendations: O(n) sorting")
    print("="*60)

if __name__ == "__main__":
    main()