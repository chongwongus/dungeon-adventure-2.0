from typing import List
from .combat_handler import CombatHandler, Combatant
from .combat_action import CombatAction


class BasicAttackHandler(CombatHandler):
    """
    Handles standard attack sequences in the combat system.

    This handler manages basic attack mechanics for characters, processing:
    - Multiple attacks based on attacker's speed
    - Hit/miss probability
    - Damage calculation
    - Blocking mechanics
    - Potential healing after attacks

    The handler supports different character types (heroes and monsters)
    and their unique combat interactions.
    """

    def execute(self, attacker: Combatant, defender: Combatant) -> List[CombatAction]:
        """
        Execute a full sequence of basic attacks for the attacker.

        Processes multiple attack attempts based on the attacker's speed,
        handling different scenarios like successful hits, blocks, and misses.

        Args:
            attacker (Combatant): The character initiating attacks
            defender (Combatant): The target of the attacks

        Returns:
            List[CombatAction]: Comprehensive list of attack actions
        """

        actions = []
        num_attacks = attacker.get_num_attacks(defender)

        for _ in range(num_attacks):
            if not defender.is_alive:
                break

            hit, damage = attacker.attack(defender)
            if hit:
                # Store HP before attack
                hp_before = defender.hp

                # Apply damage and get result
                result = defender.take_damage(damage)

                # Calculate actual damage done
                actual_damage = hp_before - defender.hp

                if isinstance(result, bool):  # Hero's take_damage returns bool
                    if result:  # Blocked
                        actions.append(CombatAction(
                            actor_name=defender.name,
                            action_type="block",
                            success=True,
                            damage=0,
                            message=f"{attacker.name} attacks but {defender.name} blocks!"
                        ))
                    else:  # Hit landing
                        actions.append(CombatAction(
                            actor_name=attacker.name,
                            action_type="attack",
                            success=True,
                            damage=actual_damage,
                            message=f"{attacker.name} hits for {actual_damage} damage!"
                        ))
                else:  # Monster's take_damage returns heal amount
                    heal_amount = result
                    # First log the damage
                    actions.append(CombatAction(
                        actor_name=attacker.name,
                        action_type="attack",
                        success=True,
                        damage=actual_damage,
                        message=f"{attacker.name} hits for {actual_damage} damage!"
                    ))
                    # Then log healing if any occurred
                    if heal_amount > 0:
                        actions.append(CombatAction(
                            actor_name=defender.name,
                            action_type="heal",
                            success=True,
                            healing=heal_amount,
                            message=f"{defender.name} heals for {heal_amount} HP!"
                        ))
            else:  # Attack missed
                actions.append(CombatAction(
                    actor_name=attacker.name,
                    action_type="attack",
                    success=False,
                    message=f"{attacker.name} misses!"
                ))

        return actions