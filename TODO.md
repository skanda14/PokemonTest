# Pokémon 1G Clone - Task Distribution

## Phase A: Overworld (Navigation & Exploration)
*Système de déplacement et interaction sur la carte.*
- [x] **Grid-based Movement**: Implémenter le déplacement case par case (16x16 pixels).
- [x] **Map Loader**: Charger les niveaux (fichiers JSON ou TMX) et les tilesets.
- [x] **Collision Manager**: Gérer les tuiles bloquantes et les "Ledges" (sauts de rebords).
- [ ] **Trigger System**: Détecter l'entrée dans les hautes herbes (`tall_grass`) pour les combats.
- [ ] **NPC Engine**: Créer des personnages statiques ou avec des routines de marche.
- [x] **Dialogue Box**: Système d'affichage de texte avec défilement ligne par ligne.

## Phase B: Battle System (Combat Engine)
*Le cœur de la logique mathématique du jeu.*
- [ ] **Battle State Manager**: Gérer la transition visuelle (flash/transition) entre l'Overworld et le Combat.
- [x] **Combatants Setup**: Charger les données du `PlayerPokemon` et de l' `EnemyPokemon`.
- [x] **Turn-based Logic**: Déterminer l'ordre d'action basé sur la statistique `speed`.
- [ ] **Action Menu**: Gérer les 4 choix (Fight, PKMN, Item, Run).
- [x] **Move Execution**: Calcul des dégâts (formule 1G), gestion des types et des PP.
- [ ] **Status Effects**: Implémenter Sleep, Burn, Paralyze, Poison, Freeze.
- [ ] **Experience & Level-up**: Calcul du gain d'XP et mise à jour des statistiques.

## Phase C: Menu & Management (UI/UX)
*L'interface utilisateur et la persistance des données.*
- [ ] **Main Start Menu**: Menu global (Pokedex, Pokemon, Item, Save).
- [ ] **Party Screen**: Affichage des 6 Pokémon de l'équipe et changement d'ordre.
- [ ] **Stats Page**: Vue détaillée d'un Pokémon (HP, Attack, Defense, Speed, Special).
- [ ] **Inventory / Bag**: Gestion des objets consommables et objets clés.
- [ ] **Save System**: Sérialisation de l'état du jeu (position, équipe, inventaire) dans un fichier.

## Phase D: Core Data (Base Technique)
*À faire en parallèle pour alimenter les autres phases.*
- [ ] **Pokemon Registry**: Dictionnaire/JSON contenant les stats de base des 151 espèces.
- [ ] **Move Set Data**: Base de données des attaques et leurs effets secondaires.
- [ ] **Type Chart**: Matrice d'efficacité des types (en respectant les spécificités de la 1G).



**Exemple Format**
- [x] **Tâche importante** (terminée)
- [ ] *Tâche régulière* (en cours)
- [ ] `Révision de code` pour le projet
- [ ] [Lien vers la documentation](https://exemple.com)
- [ ] ~~Tâche annulée~~ (barrée)