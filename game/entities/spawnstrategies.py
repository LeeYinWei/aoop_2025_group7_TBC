from game.entities.common import EnemySpawnStrategy

class OriginalSpawnStrategy(EnemySpawnStrategy):
    def should_spawn(self, et, context):
        key = (et["type"], et.get("variant", "default"))

        if et.get("is_limited", False):
            if context["spawned_counts"].get(key, 0) >= et.get("spawn_count", 0):
                return False

        return context["tower_hp_percent"] <= et.get("tower_hp_percent", 100)

    def choose_enemy_type(self, enemy_types, context):
        return enemy_types  # 全部照表跑
    
class AdvancedSpawnStrategy(EnemySpawnStrategy):
    def should_spawn(self, et, context):
        key = (et["type"], et.get("variant", "default"))

        if et.get("is_limited", False):
            if context["spawned_counts"].get(key, 0) >= et.get("spawn_count", 0):
                return False

        return context["tower_hp_percent"] <= et.get("tower_hp_percent", 100)

    def choose_enemy_type(self, enemy_types, context):
        return enemy_types  # 全部照表跑

class MLSpawnStrategy(EnemySpawnStrategy):
    def should_spawn(self, et, context):
        key = (et["type"], et.get("variant", "default"))

        if et.get("is_limited", False):
            if context["spawned_counts"].get(key, 0) >= et.get("spawn_count", 0):
                return False

        return context["tower_hp_percent"] <= et.get("tower_hp_percent", 100)

    def choose_enemy_type(self, enemy_types, context):
        return enemy_types  # 全部照表跑
