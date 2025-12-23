
class EnemySpawner:
    def __init__(self, strategy):
        self.strategy = strategy

    def update(self, current_level, enemies, enemy_types, enemy_y_manager, context):
        for et in self.strategy.choose_enemy_type(current_level.enemy_types, context):
            T = self.strategy.should_spawn(et, current_level,context)
            if not T:
                continue
            #print(f"Spawning {T} of enemy type: {et['type']}")
            for _ in range(T):
                self.spawn_enemy(et, current_level, enemies, enemy_types, enemy_y_manager, context)

    def spawn_enemy(self, et, current_level, enemies, enemy_types, enemy_y_manager, context):
        enemy_y, slot = enemy_y_manager.get_available_y()
        enemy = enemy_types[et["type"]](
            current_level.enemy_tower.x,
            enemy_y,
            is_boss=et.get("is_boss", False),
            cfg=current_level.enemy_configs.get(et["type"], {})
        )
        enemy.slot_index = slot
        enemies.append(enemy)

        key = (et["type"], et.get("variant", "default"))
        current_level.spawned_counts[key] += 1
        #print(f"Spawned enemy: {et['type']} (Total spawned: {current_level.spawned_counts[key]})")
        current_level.last_spawn_times[key] = context["time"]
