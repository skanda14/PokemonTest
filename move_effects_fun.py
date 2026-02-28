# Liste des statistiques et de leurs modificateurs pour générer le dictionnaire
stats = ["attack", "defense", "speed", "special", "accuracy", "evasion"]
modifiers = {
    "up1": {"stages": 1, "desc": "Increases {stat} by 1 stage."},
    "down1": {"stages": -1, "desc": "Decreases {stat} by 1 stage."},
    "up2": {"stages": 2, "desc": "Increases {stat} sharply by 2 stages."},
    "down2": {"stages": -2, "desc": "Decreases {stat} sharply by 2 stages."}
}

move_effects = {
    # ... (Les autres effets comme poison_effect, etc.) ...
}

# Génération dynamique des 24 effets de statistiques pour le dictionnaire
for stat in stats:
    for mod_name, mod_data in modifiers.items():
        effect_key = f"{stat}_{mod_name}_effect"

        move_effects[effect_key] = {
            "name": "modif_stat_stages",  # Le nom générique que vous avez suggéré
            "category": "residual_effects_2",
            "description": mod_data["desc"].format(stat=stat.capitalize()),
            "stat": stat,  # Nouvelle clé : la stat concernée
            "stages": mod_data["stages"]  # Nouvelle clé : la valeur numérique (-2, -1, 1, 2)
        }

# Ajout des autres effets du residual_effects_2 qui ne sont pas des stats
move_effects.update({
    "sleep_effect": {
        "name": "sleep_effect",
        "category": "residual_effects_2",
        "description": "Puts the target to sleep for 1 to 7 turns."
    },
    "bide_effect": {
        "name": "bide_effect",
        "category": "residual_effects_2",
        "description": "User waits for 2-3 turns, storing damage taken, and returns double the damage."
    }
})

###################################################################################################################

def apply_move_effect(self, effect_id, user, target):
    effect_data = move_effects.get(effect_id)

    if effect_data["name"] == "modif_stat_stages":
        stat_to_modify = effect_data["stat"]
        stages_to_add = effect_data["stages"]

        # Cible le lanceur si c'est positif (ex: Danse-Lames), ou l'adversaire si négatif (ex: Rugissement)
        target_mon = user if stages_to_add > 0 else target

        target_mon.modify_stat(stat_to_modify, stages_to_add)



###################################################################################################################



examples: {
    "attack_up1_effect": {
        "name": "modif_stat_stages",
        "category": "residual_effects_2",
        "description": "Increases Attack by 1 stage.",
        "stat": "attack",
        "stages": 1
    },
    "defense_down2_effect": {
        "name": "modif_stat_stages",
        "category": "residual_effects_2",
        "description": "Decreases Defense sharply by 2 stages.",
        "stat": "defense",
        "stages": -2
    }
}

###################################################################################################################
###################################################################################################################
###################################################################################################################

move_effects = {}

# -------------------------------------------------------------------------
# 1. STAT MODIFIERS (Générés dynamiquement)
# -------------------------------------------------------------------------
stats = ["attack", "defense", "speed", "special", "accuracy", "evasion"]
modifiers = {
    "up1": {"stages": 1, "desc": "Increases {stat} by 1 stage."},
    "down1": {"stages": -1, "desc": "Decreases {stat} by 1 stage."},
    "up2": {"stages": 2, "desc": "Increases {stat} sharply by 2 stages."},
    "down2": {"stages": -2, "desc": "Decreases {stat} sharply by 2 stages."}
}

for stat in stats:
    for mod_name, mod_data in modifiers.items():
        move_effects[f"{stat}_{mod_name}_effect"] = {
            "name": "modify_stat",
            "category": "residual_effects_2",
            "description": mod_data["desc"].format(stat=stat.capitalize()),
            "stat": stat,
            "stages": mod_data["stages"]
        }

# -------------------------------------------------------------------------
# 2. STATUS CONDITIONS (Poison, Paralyze, Sleep...)
# -------------------------------------------------------------------------
statuses = {
    "poison_effect": {"status": "poison", "category": "residual_effects_1"},
    "paralyze_effect": {"status": "paralyze", "category": "residual_effects_1"},
    "sleep_effect": {"status": "sleep", "category": "residual_effects_2"}
}

for effect_key, data in statuses.items():
    move_effects[effect_key] = {
        "name": "inflict_status",
        "category": data["category"],
        "description": f"Inflicts {data['status']} on the target.",
        "status": data["status"],
        "chance": 1.0  # 100% chance (pour les attaques de statut principal comme Toxik ou Poudre Dodo)
    }

# -------------------------------------------------------------------------
# 3. MULTI-HIT MOVES
# -------------------------------------------------------------------------
multi_hits = {
    "two_to_five_attacks_effect": {"min": 2, "max": 5, "desc": "Hits the target 2 to 5 times."},
    "attack_twice_effect": {"min": 2, "max": 2, "desc": "Hits the target exactly twice."},
    "effect_1e": {"min": 2, "max": 2, "desc": "Hits the target exactly twice (Double Kick)."}
}

for effect_key, data in multi_hits.items():
    move_effects[effect_key] = {
        "name": "multi_hit",
        "category": "always_happen_effects",
        "description": data["desc"],
        "min_hits": data["min"],
        "max_hits": data["max"]
    }

# Ajout manuel de Twineedle (qui est une attaque multiple avec un effet secondaire de statut)
move_effects["twineedle_effect"] = {
    "name": "multi_hit",
    "category": "always_happen_effects",
    "description": "Hits twice. Has a 20% chance to poison the target.",
    "min_hits": 2,
    "max_hits": 2,
    "secondary_effect": {
        "name": "inflict_status",
        "status": "poison",
        "chance": 0.2
    }
}

# -------------------------------------------------------------------------
# 4. HP DRAIN & RECOIL MOVES
# -------------------------------------------------------------------------
move_effects.update({
    "drain_hp_effect": {
        "name": "drain_hp",
        "category": "always_happen_effects",
        "description": "Heals the user by 50% of the damage dealt.",
        "heal_fraction": 0.5,
        "requires_target_status": None
    },
    "dream_eater_effect": {
        "name": "drain_hp",
        "category": "always_happen_effects",
        "description": "Fails unless the target is asleep. Drains 50% of damage.",
        "heal_fraction": 0.5,
        "requires_target_status": "sleep" # Condition spécifique à Dream Eater
    },
    "recoil_effect": {
        "name": "recoil",
        "category": "always_happen_effects",
        "description": "User takes 1/4 of the damage dealt as recoil.",
        "recoil_fraction": 0.25
    },
    "jump_kick_effect": {
        "name": "crash_damage",
        "category": "special_effects",
        "description": "If the move misses, the user takes 1 HP crash damage.",
        "crash_damage_on_miss": 1
    }
})

# -------------------------------------------------------------------------
# 5. FIXED & SPECIAL DAMAGE
# -------------------------------------------------------------------------
move_effects.update({
    "super_fang_effect": {
        "name": "fixed_damage",
        "category": "set_damage_effects",
        "description": "Halves the target's current HP.",
        "damage_type": "halve_current_hp"
    },
    "special_damage_effect": {
        "name": "fixed_damage",
        "category": "set_damage_effects",
        "description": "Deals fixed or level-based damage.",
        "damage_type": "level_or_fixed" # Dans le code, dépend de wPlayerMoveNum
    }
})

# -------------------------------------------------------------------------
# 6. OTHER UNIQUE BEHAVIORS
# -------------------------------------------------------------------------
move_effects.update({
    "charge_effect": {
        "name": "two_turn_move",
        "category": "special_effects",
        "description": "Charges on turn 1, attacks on turn 2.",
        "invulnerable_during_charge": False
    },
    "fly_effect": {
        "name": "two_turn_move",
        "category": "special_effects",
        "description": "User becomes invulnerable on turn 1, attacks on turn 2.",
        "invulnerable_during_charge": True
    },
    "swift_effect": {
        "name": "bypass_accuracy",
        "category": "special_effects",
        "description": "Never misses, bypassing accuracy checks.",
        "always_hits": True
    }
    # Les autres effets très spécifiques (Metronome, Transform, etc.) garderaient
    # des "name" uniques car leur logique est impossible à généraliser.
})

###################################################################################################################


def apply_effect(self, effect_key, user, target, damage_dealt=0):
    effect = move_effects.get(effect_key)
    if not effect:
        return

    eff_name = effect["name"]

    # 1. Gestion des modificateurs de stats
    if eff_name == "modify_stat":
        stat_target = user if effect["stages"] > 0 else target
        stat_target.modify_stat(effect["stat"], effect["stages"])

    # 2. Gestion des altérations de statut
    elif eff_name == "inflict_status":
        if random.random() <= effect["chance"]:
            target.apply_status(effect["status"])

    # 3. Gestion du vol de vie (Drain)
    elif eff_name == "drain_hp":
        # Vérifie si le drain nécessite un statut (ex: cible endormie pour Dévorêve)
        req_status = effect.get("requires_target_status")
        if req_status and target.status != req_status:
            print("But it failed!")
            return

        heal_amount = max(1, int(damage_dealt * effect["heal_fraction"]))
        user.heal(heal_amount)
        print(f"{user.name} had its energy drained!")

    # 4. Gestion des dégâts de recul
    elif eff_name == "recoil":
        recoil_dmg = max(1, int(damage_dealt * effect["recoil_fraction"]))
        user.take_damage(recoil_dmg)
        print(f"{user.name} is hit with recoil!")