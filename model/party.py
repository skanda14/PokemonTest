class Party:
    def __init__(self):
        self.members = []

    def get_first_member(self):
        return self.members[0]

    def add_a_member(self, member):
        self.members.append(member)

    def remove_a_member(self, member):
        self.members.remove(member)

    def swap_pokemon(self, index_1, index_2):
        # Swaps two Pokemon in the team. Returns True if successful.
        try: # Vérification que les indices sont valides
            self.members[index_1], self.members[index_2] = self.members[index_2], self.members[index_1]
            return True
        except IndexError:
            print(f"Error: Indices {index_1} or {index_2} are out of range.")
            return False