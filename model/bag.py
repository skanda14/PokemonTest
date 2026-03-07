MAX_STACK_SIZE = 99

class InventorySlot:
    def __init__(self, item_id, quantity=1, is_key_item=False):
        self.item_id = item_id
        self.item_name = "ITEM"+str(self.item_id)
        self.quantity = quantity
        self.is_key_item = is_key_item

    def modify_quantity(self, n):
        self.quantity = min(MAX_STACK_SIZE, max(self.quantity+n, 0))


class Bag:
    def __init__(self):
        self.slots = []  # List of InventorySlot objects
        self.MAX_SLOTS = 20

    def can_receive_item(self, item_id, amount=1, is_key_item=False):
        """
        Vérifie si le sac peut accueillir la TOTALITÉ de la quantité demandée.
        """
        # 1. Cas des Key Items (règle Gen I : un seul exemplaire max par slot)
        if is_key_item:
            if any(s.item_id == item_id for s in self.slots):
                return False  # Déjà possédé
            return len(self.slots) < self.MAX_SLOTS

        # 2. Calcul de la capacité totale pour cet objet précis
        total_capacity = 0

        # Espace dans les stacks existants du même objet
        for slot in self.slots:
            if slot.item_id == item_id:
                total_capacity += (MAX_STACK_SIZE - slot.quantity)

        # Espace dans les slots entièrement vides
        empty_slots = self.MAX_SLOTS - len(self.slots)
        total_capacity += (empty_slots * MAX_STACK_SIZE)
        return total_capacity >= amount

    def add_item(self, item_id, amount=1, is_key_item=False):
        """
        Adds an item to the bag, splitting it into multiple stacks if needed.
        Assumes can_receive_item() was called beforehand.
        """
        # 1. Traitement spécifique pour les Key Items
        if is_key_item:
            # On vérifie quand même s'il n'est pas déjà là (Sécurité Model)
            if not any(slot.item_id == item_id for slot in self.slots):
                if len(self.slots) < self.MAX_SLOTS:
                    self.slots.append(InventorySlot(item_id, 1, is_key_item=True))
                    return True
            return False

        # 2. Remplir les piles existantes (< 99)
        for slot in self.slots:
            if slot.item_id == item_id and slot.quantity < MAX_STACK_SIZE:
                space_left = MAX_STACK_SIZE - slot.quantity
                to_add = min(amount, space_left)
                slot.quantity += to_add
                amount -= to_add

            if amount <= 0: return True  # Tout a été placé

        # 3. Créer de nouveaux slots pour le surplus
        while amount > 0 and len(self.slots) < self.MAX_SLOTS:
            to_add = min(amount, MAX_STACK_SIZE)
            self.slots.append(InventorySlot(item_id, to_add))
            amount -= to_add

        # Retourne True si tout l'amount a été distribué, False sinon
        return amount == 0

    def toss_item(self, slot_index, amount):
        """
        Removes a specific quantity from a slot.
        If quantity reaches 0, the slot is removed from the bag.
        """
        # 1. Sécurité : Vérifier si l'index existe
        if slot_index < 0 or slot_index >= len(self.slots):
            return False

        target_slot = self.slots[slot_index]

        # 2. Règle Gen I : Impossible de jeter un Key Item
        if target_slot.is_key_item:
            return False

        # 3. Réduction de la quantité
        # On ne peut pas jeter plus que ce qu'on a dans ce slot précis
        actual_to_remove = min(amount, target_slot.quantity)
        target_slot.quantity -= actual_to_remove

        # 4. Nettoyage : Si le slot est vide, on le supprime de la liste
        if target_slot.quantity <= 0:
            self.slots.pop(slot_index)

        return True
