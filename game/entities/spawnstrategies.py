from game.entities.common import EnemySpawnStrategy

class OriginalSpawnStrategy(EnemySpawnStrategy):
    def should_spawn(self, et, current_level,context):
        key = (et["type"], et.get("variant", "default"))

        interval = et.get("spawn_interval_1", current_level.spawn_interval)
        initial_delay = et.get("initial_delay", 0)

        if context["time"] - current_level.last_spawn_times.get(key, 0) < interval:
            return False
        if context["time"] - context["level_start_time"] < initial_delay:
            return False

        if et.get("is_limited", False):
            if context["spawned_counts"].get(key, 0) >= et.get("spawn_count", 0):
                return False

        return context["tower_hp_percent"] <= et.get("tower_hp_percent", 100)

    def choose_enemy_type(self, enemy_types, context):
        return enemy_types  # 全部照表跑
    
class AdvancedSpawnStrategy(EnemySpawnStrategy):
    def should_spawn(self, et, current_level, context):
        key = (et["type"], et.get("variant", "default"))

        interval = et.get("spawn_interval_1", current_level.spawn_interval)*context["tower_hp_percent"]/100# effective interval scales with tower HP
        initial_delay = et.get("initial_delay", 0)

        if context["time"] - current_level.last_spawn_times.get(key, 0) < interval:
            return False
        if context["time"] - context["level_start_time"] < initial_delay:
            return False

        if et.get("is_limited", False):
            if context["spawned_counts"].get(key, 0) >= et.get("spawn_count", 0):
                return False

        return context["tower_hp_percent"] <= et.get("tower_hp_percent", 100)

    def choose_enemy_type(self, enemy_types, context):
        return enemy_types  # 全部照表跑


class MLSpawnStrategy(EnemySpawnStrategy):# trash
    def should_spawn(self, et, context):
        key = (et["type"], et.get("variant", "default"))

        if et.get("is_limited", False):
            if context["spawned_counts"].get(key, 0) >= et.get("spawn_count", 0):
                return False

        return context["tower_hp_percent"] <= et.get("tower_hp_percent", 100)

    def choose_enemy_type(self, enemy_types, context):
        return enemy_types  # 全部照表跑
